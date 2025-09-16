import easyocr
import cv2
import numpy as np
from typing import Dict, Optional, Tuple, List
import re
import time
import threading
import math
from scipy import ndimage

class IDCardReader:
    def __init__(self):
        # Инициализация EasyOCR с поддержкой русского и белорусского языков
        self.reader = easyocr.Reader(['ru', 'be'])
        # Константы для шаблонного анализа
        self.id_card_ratio = 1.6  # Соотношение сторон ID-карты
        
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Предобработка изображения для улучшения качества распознавания"""
        # Преобразование в оттенки серого
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Увеличение контраста
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrast = clahe.apply(gray)
        # Удаление шума
        denoised = cv2.fastNlMeansDenoising(contrast)
        return denoised
    
    def advanced_preprocess(self, image: np.ndarray) -> np.ndarray:
        """Расширенная предобработка изображения"""
        # Конвертируем в оттенки серого
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Применяем адаптивную бинаризацию для улучшения контраста текста
        # Это особенно помогает при неравномерном освещении
        bin_img = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Применяем морфологические операции для усиления текста
        kernel = np.ones((1, 1), np.uint8)
        morphed = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)
        
        # Увеличение контраста
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        contrast = clahe.apply(gray)
        
        # Применяем Гауссово размытие для уменьшения шума
        blurred = cv2.GaussianBlur(contrast, (3, 3), 0)
        
        # Удаление шума с сохранением краев
        denoised = cv2.fastNlMeansDenoising(blurred, None, 10, 7, 21)
        
        return denoised
    
    def detect_card_boundaries(self, image: np.ndarray) -> Tuple[np.ndarray, bool]:
        """Обнаружение границ карты на изображении"""
        # Создаем копию изображения
        img_copy = image.copy()
        
        # Преобразуем в оттенки серого
        gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        
        # Размытие для уменьшения шума
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Применяем Canny для обнаружения краев
        edges = cv2.Canny(blur, 50, 150)
        
        # Находим контуры
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Если контуры не найдены, возвращаем оригинальное изображение
        if not contours:
            return image, False
        
        # Находим самый большой контур (предположительно, это ID-карта)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Проверяем, достаточно ли большой контур (минимум 50% площади изображения)
        img_area = image.shape[0] * image.shape[1]
        contour_area = cv2.contourArea(largest_contour)
        if contour_area < img_area * 0.3:
            return image, False
            
        # Аппроксимируем контур многоугольником
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        
        # Проверяем, что у нас 4 точки (прямоугольник)
        if len(approx) == 4:
            # Сортируем точки для правильного порядка
            points = np.array([p[0] for p in approx])
            points = self.order_points(points)
            
            # Вычисляем новые размеры
            width_a = np.sqrt(((points[2][0] - points[3][0]) ** 2) + ((points[2][1] - points[3][1]) ** 2))
            width_b = np.sqrt(((points[1][0] - points[0][0]) ** 2) + ((points[1][1] - points[0][1]) ** 2))
            max_width = max(int(width_a), int(width_b))
            
            height_a = np.sqrt(((points[1][0] - points[2][0]) ** 2) + ((points[1][1] - points[2][1]) ** 2))
            height_b = np.sqrt(((points[0][0] - points[3][0]) ** 2) + ((points[0][1] - points[3][1]) ** 2))
            max_height = max(int(height_a), int(height_b))
            
            # Корректируем соотношение сторон, если нужно
            if max_width / max_height > 2.0 or max_height / max_width > 2.0:
                return image, False
            
            # Цель преобразования
            dst = np.array([
                [0, 0],
                [max_width - 1, 0],
                [max_width - 1, max_height - 1],
                [0, max_height - 1]
            ], dtype="float32")
            
            # Вычисляем матрицу трансформации
            transform_matrix = cv2.getPerspectiveTransform(points.astype("float32"), dst)
            
            # Применяем трансформацию перспективы
            warped = cv2.warpPerspective(image, transform_matrix, (max_width, max_height))
            
            return warped, True
        
        return image, False
    
    def order_points(self, pts: np.ndarray) -> np.ndarray:
        """Упорядочивание точек прямоугольника [top-left, top-right, bottom-right, bottom-left]"""
        rect = np.zeros((4, 2), dtype="float32")
        
        # Сумма координат - минимальна для верхнего левого угла, максимальна для нижнего правого
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # Разность между точками: минимальна для верхнего правого, максимальна для нижнего левого
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        return rect
    
    def deskew_image(self, image: np.ndarray) -> np.ndarray:
        """Выравнивание изображения по горизонтали"""
        try:
            # Преобразование в оттенки серого
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Бинаризация изображения
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            
            # Вычисление угла наклона
            coords = np.column_stack(np.where(thresh > 0))
            if len(coords) == 0:
                return image  # Если нет текста, возвращаем исходное изображение
                
            angle = cv2.minAreaRect(coords)[-1]
            
            # Корректировка угла
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
                
            # Вращаем только если угол значительный
            if abs(angle) > 0.5:
                (h, w) = image.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                return rotated
                
            return image
        except Exception as e:
            # В случае ошибки возвращаем исходное изображение
            print(f"Ошибка при выравнивании изображения: {str(e)}")
            return image
        
    def extract_fields(self, text_results: list) -> Dict[str, str]:
        """Извлечение нужных полей из распознанного текста"""
        fields = {
            'insurance_number': None,
            'surname_be': None,
            'surname_ru': None,
            'name_be': None,
            'name_ru': None,
            'patronymic_be': None,
            'patronymic_ru': None,
            'gender_be': None,
            'gender_ru': None,
            'birth_date': None
        }
        
        # Поиск страхового номера с помощью регулярного выражения
        full_text = ' '.join([detection[1] for detection in text_results])
        insurance_pattern = r'[0-9]{7}[A-Z][0-9]{3}[A-Z]{2}[0-9]'
        insurance_match = re.search(insurance_pattern, full_text)
        if insurance_match:
            fields['insurance_number'] = insurance_match.group(0)
        
        # Словарь для соответствия исходного текста и возможных вариантов ошибок
        field_keywords = {
            'surname_be': ['прозвішча', 'прозвiшча', 'npозвiшча'],
            'surname_ru': ['фамилия', 'фамипия', 'фамилня'],
            'name_be': ['уласнае імя', 'імя', 'уласнае iмя', 'iмя'],
            'name_ru': ['собственное имя', 'имя', 'собственное'],
            'patronymic_be': ['імя па бацьку', 'iмя па бацьку', 'бацьку'],
            'patronymic_ru': ['отчество', 'отч'],
            'gender': ['пол', 'non'],
            'birth_date': ['нараджэння', 'рождения', 'дата']
        }
        
        # Организуем данные по координатам для анализа структуры документа
        structured_data = {}
        for detection in text_results:
            bbox = detection[0]  # Координаты bbox: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            text = detection[1]
            y_center = sum([p[1] for p in bbox]) / 4  # Среднее значение y
            structured_data[text] = {'y': y_center, 'bbox': bbox}
        
        # Теперь можем искать значения полей, зная их относительное положение
        for i, detection in enumerate(text_results):
            text = detection[1].lower()
            original_text = detection[1]
            
            # Поиск страхового номера (если не найден через регулярку)
            if any(keyword in text for keyword in ['страхавы', 'страховой']) and fields['insurance_number'] is None:
                # Ищем значение справа или на следующей строке
                for other_text, props in structured_data.items():
                    if re.match(insurance_pattern, other_text):
                        fields['insurance_number'] = other_text
                        break
            
            # Поиск фамилии, имени и отчества
            for field_key, keywords in field_keywords.items():
                if any(keyword in text for keyword in keywords):
                    # Базовый y-центр текущего поля
                    base_y = structured_data[detection[1]]['y']
                    
                    # Ищем ближайший текст справа или на той же строке
                    candidate_value = None
                    min_distance = float('inf')
                    
                    for other_text, props in structured_data.items():
                        if other_text == detection[1]:
                            continue
                            
                        # Если текст примерно на том же уровне (±5 пикселей)
                        if abs(props['y'] - base_y) < 15:
                            # Проверяем, что текст находится правее
                            current_bbox = structured_data[detection[1]]['bbox']
                            other_bbox = props['bbox']
                            
                            # Если правый край текущего поля левее левого края другого текста
                            if max(p[0] for p in current_bbox) < min(p[0] for p in other_bbox):
                                # Вычисляем горизонтальное расстояние
                                dist = min(p[0] for p in other_bbox) - max(p[0] for p in current_bbox)
                                
                                if dist < min_distance:
                                    min_distance = dist
                                    candidate_value = other_text
                    
                    # Если нашли кандидата и он в пределах разумного расстояния
                    if candidate_value and min_distance < 200:
                        if field_key == 'surname_be':
                            fields['surname_be'] = candidate_value
                        elif field_key == 'surname_ru':
                            fields['surname_ru'] = candidate_value
                        elif field_key == 'name_be':
                            fields['name_be'] = candidate_value
                        elif field_key == 'name_ru':
                            fields['name_ru'] = candidate_value
                        elif field_key == 'patronymic_be':
                            fields['patronymic_be'] = candidate_value
                        elif field_key == 'patronymic_ru':
                            fields['patronymic_ru'] = candidate_value
                        elif field_key == 'gender':
                            if 'жаночы' in candidate_value.lower():
                                fields['gender_be'] = 'жаночы'
                            elif 'женский' in candidate_value.lower():
                                fields['gender_ru'] = 'женский'
                            elif 'мужчынскі' in candidate_value.lower():
                                fields['gender_be'] = 'мужчынскі'
                            elif 'мужской' in candidate_value.lower():
                                fields['gender_ru'] = 'мужской'
                        elif field_key == 'birth_date':
                            date_pattern = r'\d{2}\.\d{2}\.\d{4}'
                            date_match = re.search(date_pattern, candidate_value)
                            if date_match:
                                fields['birth_date'] = date_match.group(0)
            
            # Прямой поиск значений пола
            if 'жаночы' in text:
                fields['gender_be'] = 'жаночы'
            elif 'женский' in text:
                fields['gender_ru'] = 'женский'
            elif 'мужчынскі' in text:
                fields['gender_be'] = 'мужчынскі'
            elif 'мужской' in text:
                fields['gender_ru'] = 'мужской'
            
            # Прямой поиск даты
            date_pattern = r'\d{2}\.\d{2}\.\d{4}'
            date_match = re.search(date_pattern, original_text)
            if date_match and fields['birth_date'] is None:
                fields['birth_date'] = date_match.group(0)
        
        # Применяем постобработку для повышения точности
        fields = self.postprocess_fields(fields, text_results)
        
        return fields
    
    def postprocess_fields(self, fields: Dict[str, str], text_results: list) -> Dict[str, str]:
        """Постобработка распознанных полей для повышения точности"""
        # Проверка формата страхового номера
        if fields['insurance_number']:
            # Должен соответствовать шаблону XXXXXXXAXXXPBX
            if not re.match(r'[0-9]{7}[A-Z][0-9]{3}[A-Z]{2}[0-9]', fields['insurance_number']):
                # Исправляем распространенные ошибки распознавания
                corrected = fields['insurance_number']
                corrected = corrected.replace('O', '0').replace('I', '1').replace('l', '1')
                if re.match(r'[0-9]{7}[A-Z][0-9]{3}[A-Z]{2}[0-9]', corrected):
                    fields['insurance_number'] = corrected
        
        # Проверка и коррекция даты рождения
        if fields['birth_date']:
            # Проверяем формат даты
            if re.match(r'\d{2}\.\d{2}\.\d{4}', fields['birth_date']):
                try:
                    day, month, year = map(int, fields['birth_date'].split('.'))
                    # Проверяем валидность даты
                    if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2023):
                        fields['birth_date'] = None
                except:
                    fields['birth_date'] = None
        
        # Проверка корректности распознавания имени/фамилии (простые проверки)
        for field in ['surname_ru', 'surname_be', 'name_ru', 'name_be', 'patronymic_ru', 'patronymic_be']:
            if fields[field]:
                # Если поле содержит числа или специальные символы, вероятно ошибка
                if re.search(r'[0-9]', fields[field]) or re.search(r'[!@#$%^&*()_+={}\[\]:;<>,.?/\\|]', fields[field]):
                    fields[field] = None
        
        return fields

    def quick_analyze_image(self, image: np.ndarray) -> list:
        """Быстрый анализ изображения для промежуточного вывода"""
        # Упрощенная предобработка для скорости
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Увеличение контраста для лучшего распознавания
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrast = clahe.apply(gray)
        # Вызываем распознавание с упрощенными настройками
        results = self.reader.readtext(contrast, detail=1, paragraph=False)
        return results

    def camera_capture_and_process(self, cap=None, close_camera=False) -> Tuple[Dict[str, str], object]:
        """Захват изображения с камеры и обработка"""
        camera_was_opened = False
        
        # Если камера не была передана, открываем новую
        if cap is None:
            cap = cv2.VideoCapture(0)
            camera_was_opened = True
            
            if not cap.isOpened():
                raise ValueError("Не удалось открыть камеру")
                
            print("Подготовка камеры...")
            # Даем камере время на инициализацию
            for i in range(10):
                ret, frame = cap.read()
                if i == 9:
                    print("Камера готова!")
        
        print("Поднесите ID-карту к камере и держите ровно")
        
        # Определяем размеры кадра
        ret, frame = cap.read()
        if not ret:
            raise ValueError("Не удалось получить кадр с камеры")
            
        frame_height, frame_width = frame.shape[:2]
            
        # Создаем прямоугольник для позиционирования документа (85% от ширины кадра)
        rect_width = int(frame_width * 0.85)
        rect_height = int(rect_width * 0.6)  # ID-карты обычно имеют соотношение ~1.6:1
        rect_x = (frame_width - rect_width) // 2
        rect_y = (frame_height - rect_height) // 2
        
        # Переменные для промежуточного распознавания
        last_analysis_time = time.time()
        current_detected_text = []
        
        # Переменная для хранения промежуточных результатов распознавания
        live_detected_fields = {
            'insurance_number': None,
            'name': None,
            'surname': None,
            'birth_date': None
        }
        
        # Флаг для автоматического определения документа
        auto_detection_active = True
        detected_card = None
        
        # Функция для асинхронного распознавания текста
        def analyze_image_async(img):
            nonlocal current_detected_text, auto_detection_active, detected_card
            
            # Пытаемся автоматически определить границы карты
            if auto_detection_active:
                warped_img, success = self.detect_card_boundaries(img)
                if success:
                    detected_card = warped_img
                    # Используем обнаруженную карту для распознавания
                    detected_text = self.quick_analyze_image(warped_img)
                    current_detected_text = detected_text
                    
                    # Обновляем промежуточные результаты
                    update_live_fields(detected_text)
                    return
            
            # Если автоопределение не удалось, используем рамку
            cropped = img[rect_y:rect_y+rect_height, rect_x:rect_x+rect_width]
            # Применяем выравнивание текста
            deskewed = self.deskew_image(cropped)
            detected_text = self.quick_analyze_image(deskewed)
            current_detected_text = detected_text
            
            # Обновляем промежуточные результаты
            update_live_fields(detected_text)
        
        # Функция для обновления промежуточных результатов
        def update_live_fields(detected_text):
            nonlocal live_detected_fields
            
            # Объединяем весь текст для поиска страхового номера
            full_text = ' '.join([det[1] for det in detected_text])
            
            # Ищем страховой номер
            insurance_pattern = r'[0-9]{7}[A-Z][0-9]{3}[A-Z]{2}[0-9]'
            insurance_match = re.search(insurance_pattern, full_text)
            if insurance_match:
                live_detected_fields['insurance_number'] = insurance_match.group(0)
            
            # Ищем дату рождения
            date_pattern = r'\d{2}\.\d{2}\.\d{4}'
            date_match = re.search(date_pattern, full_text)
            if date_match:
                live_detected_fields['birth_date'] = date_match.group(0)
            
            # Проверяем наличие ключевых слов для имени и фамилии
            for text_det in detected_text:
                text = text_det[1].lower()
                if 'фамилия' in text or 'прозвішча' in text:
                    for t in detected_text:
                        if t != text_det and len(t[1]) < 20:  # Имя/фамилия обычно короткие
                            live_detected_fields['surname'] = t[1]
                            break
                            
                if 'имя' in text or 'собственное имя' in text or 'уласнае імя' in text:
                    for t in detected_text:
                        if t != text_det and len(t[1]) < 20:
                            live_detected_fields['name'] = t[1]
                            break
        
        # Флаг для активного анализа
        analysis_active = False
        
        while True:
            ret, frame = cap.read()
            if not ret:
                raise ValueError("Не удалось получить кадр с камеры")
                
            # Копируем кадр для отображения
            display_frame = frame.copy()
            
            # Промежуточное распознавание каждую секунду
            current_time = time.time()
            if current_time - last_analysis_time > 1.0 and not analysis_active:
                last_analysis_time = current_time
                analysis_active = True
                # Запускаем распознавание в отдельном потоке
                analysis_thread = threading.Thread(target=analyze_image_async, args=(frame.copy(),))
                analysis_thread.daemon = True
                analysis_thread.start()
                analysis_active = False
            
            # Если карта была обнаружена автоматически, показываем ее контур
            if detected_card is not None and auto_detection_active:
                # Показываем миниатюру обнаруженной карты
                thumbnail_size = (int(frame_width * 0.3), int(frame_height * 0.3))
                thumbnail = cv2.resize(detected_card, thumbnail_size)
                
                # Размещаем миниатюру в правом верхнем углу
                x_offset = frame_width - thumbnail_size[0] - 10
                y_offset = 10
                display_frame[y_offset:y_offset+thumbnail_size[1], x_offset:x_offset+thumbnail_size[0]] = thumbnail
                
                # Добавляем текст "Обнаружена карта"
                cv2.putText(display_frame, "Карта обнаружена", 
                           (x_offset, y_offset + thumbnail_size[1] + 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                # Рисуем рамку для позиционирования вручную
                cv2.rectangle(display_frame, (rect_x, rect_y), 
                             (rect_x + rect_width, rect_y + rect_height), 
                             (0, 255, 0), 2)
            
            # Добавляем инструкции
            cv2.putText(display_frame, "Выровняйте ID-карту по рамке", 
                        (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(display_frame, "Нажмите ПРОБЕЛ для захвата", 
                        (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(display_frame, "Нажмите ESC для выхода", 
                        (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(display_frame, "Нажмите 'A' для вкл/выкл автоопределения", 
                        (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Отображаем обнаруженный текст в реальном времени
            y_offset = 150
            cv2.putText(display_frame, "Что видит нейронка:", 
                        (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            y_offset += 30
            
            # Отображаем промежуточные результаты
            for field, value in live_detected_fields.items():
                if value:
                    field_name = {
                        'insurance_number': 'Страховой номер',
                        'name': 'Имя',
                        'surname': 'Фамилия',
                        'birth_date': 'Дата рождения'
                    }.get(field, field)
                    
                    cv2.putText(display_frame, f"{field_name}: {value}", 
                               (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
                    y_offset += 25
            
            # Отображаем распознанный текст (первые 5 элементов)
            if current_detected_text:
                y_offset += 10
                cv2.putText(display_frame, "Распознанный текст:", 
                           (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
                y_offset += 25
                
                for i, text_item in enumerate(current_detected_text[:5]):
                    text = text_item[1]
                    if len(text) > 25:
                        text = text[:22] + "..."
                    cv2.putText(display_frame, text, 
                               (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    y_offset += 20
                    if y_offset > frame_height - 20:
                        break
            
            # Показываем индикатор степени уверенности в распознавании
            confidence_level = self.calculate_confidence_level(live_detected_fields)
            confidence_color = (0, 255, 0) if confidence_level > 70 else (0, 165, 255) if confidence_level > 40 else (0, 0, 255)
            
            cv2.putText(display_frame, f"Уверенность: {confidence_level}%", 
                      (frame_width - 250, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, confidence_color, 2)
            
            # Рисуем индикатор уверенности
            bar_width = 200
            bar_height = 15
            bar_x = frame_width - 250
            bar_y = 50
            
            # Фон индикатора
            cv2.rectangle(display_frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (120, 120, 120), -1)
            # Заполнение индикатора
            filled_width = int(bar_width * confidence_level / 100)
            cv2.rectangle(display_frame, (bar_x, bar_y), (bar_x + filled_width, bar_y + bar_height), confidence_color, -1)
            
            cv2.imshow('Распознавание ID-карты', display_frame)
            
            key = cv2.waitKey(1)
            if key == 32:  # Пробел
                print("Фотографирую... Не двигайтесь!")
                
                # Делаем несколько снимков для лучшего результата
                frames = []
                for _ in range(3):
                    ret, img = cap.read()
                    if ret:
                        frames.append(img)
                    cv2.waitKey(300)  # Небольшая задержка между снимками
                
                # Применяем технику HDR для улучшения качества изображения
                best_frame = self.blend_frames(frames) if len(frames) > 1 else frames[0]
                
                # Используем обнаруженную карту если есть, иначе вырезаем по рамке
                if detected_card is not None and auto_detection_active:
                    cropped_frame = detected_card
                else:
                    cropped_frame = best_frame[rect_y:rect_y+rect_height, rect_x:rect_x+rect_width]
                    # Применяем выравнивание
                    cropped_frame = self.deskew_image(cropped_frame)
                
                # Сохраняем кадр с уникальным именем
                timestamp = int(time.time())
                save_path = f'captured_id_card_{timestamp}.jpg'
                cv2.imwrite(save_path, cropped_frame)
                print(f"Изображение сохранено как {save_path}")
                
                # Закрываем окно отображения, но не закрываем камеру
                cv2.destroyAllWindows()
                
                # Если запрос закрытия камеры, закрываем
                if close_camera and camera_was_opened:
                    cap.release()
                
                # Обрабатываем изображение с расширенной предобработкой
                processed_image = self.advanced_preprocess(cropped_frame)
                results = self.reader.readtext(processed_image)
                fields = self.extract_fields(results)
                
                return fields, cap
            
            elif key == 97:  # 'a' для вкл/выкл автоопределения
                auto_detection_active = not auto_detection_active
                print(f"Автоопределение границ карты: {'Включено' if auto_detection_active else 'Выключено'}")
                if not auto_detection_active:
                    detected_card = None
                    
            elif key == 27:  # ESC для выхода
                break
                
        # Закрываем окно и освобождаем камеру, если мы её открывали
        cv2.destroyAllWindows()
        if camera_was_opened:
            cap.release()
            
        raise ValueError("Операция была отменена")

    def blend_frames(self, frames: List[np.ndarray]) -> np.ndarray:
        """Объединение нескольких кадров для улучшения качества (простой HDR)"""
        if not frames:
            return None
            
        # Если только один кадр, возвращаем его
        if len(frames) == 1:
            return frames[0]
            
        # Выравниваем кадры относительно первого
        aligned_frames = []
        aligned_frames.append(frames[0])
        
        # Преобразуем первый кадр в оттенки серого для сравнения
        first_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        
        for i in range(1, len(frames)):
            # Преобразуем текущий кадр в оттенки серого
            current_gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            
            # Находим матрицу гомографии между кадрами
            try:
                # Используем ORB для обнаружения ключевых точек
                orb = cv2.ORB_create()
                kp1, des1 = orb.detectAndCompute(first_gray, None)
                kp2, des2 = orb.detectAndCompute(current_gray, None)
                
                # Используем BFMatcher для сопоставления точек
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(des1, des2)
                
                # Сортируем по расстоянию
                matches = sorted(matches, key=lambda x: x.distance)
                
                # Берем лучшие совпадения (не больше 30)
                good_matches = matches[:min(30, len(matches))]
                
                if len(good_matches) >= 4:
                    # Получаем координаты точек
                    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                    
                    # Вычисляем матрицу гомографии
                    H, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
                    
                    # Применяем трансформацию к текущему кадру
                    h, w = first_gray.shape
                    aligned = cv2.warpPerspective(frames[i], H, (w, h))
                    aligned_frames.append(aligned)
                else:
                    # Если недостаточно совпадений, используем оригинальный кадр
                    aligned_frames.append(frames[i])
            except Exception as e:
                # При ошибке используем оригинальный кадр
                aligned_frames.append(frames[i])
        
        # Вычисляем средний кадр
        result = np.zeros_like(frames[0], dtype=np.float32)
        for frame in aligned_frames:
            result += frame.astype(np.float32)
        
        result /= len(aligned_frames)
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return result
    
    def calculate_confidence_level(self, detected_fields: Dict[str, str]) -> int:
        """Вычисляет уровень уверенности в распознавании на основе заполненных полей"""
        # Веса полей по важности
        field_weights = {
            'insurance_number': 40,  # Страховой номер наиболее важен
            'name': 20,              # Имя
            'surname': 20,           # Фамилия
            'birth_date': 20         # Дата рождения
        }
        
        total_weight = sum(field_weights.values())
        current_score = 0
        
        for field, weight in field_weights.items():
            if field in detected_fields and detected_fields[field] is not None:
                current_score += weight
        
        confidence = (current_score / total_weight) * 100
        return int(confidence)

    def read_card(self, image_path: str) -> Dict[str, str]:
        """Основной метод для чтения данных с карточки"""
        # Загрузка изображения
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Не удалось загрузить изображение")
            
        # Пытаемся автоматически определить границы карты
        warped_image, success = self.detect_card_boundaries(image)
        if success:
            image = warped_image
            
        # Выравниваем изображение
        deskewed_image = self.deskew_image(image)
            
        # Предобработка с улучшенными алгоритмами
        processed_image = self.advanced_preprocess(deskewed_image)
        
        # Распознавание текста
        results = self.reader.readtext(processed_image)
        
        # Извлечение полей
        fields = self.extract_fields(results)
        
        return fields

def main():
    # Пример использования
    reader = IDCardReader()
    try:
        print("1. Сделать снимок с камеры")
        print("2. Загрузить изображение из файла")
        choice = input("Выберите опцию (1 или 2): ")
        
        if choice == '1':
            # Режим последовательного сканирования
            print("\nРежим последовательного сканирования карт")
            print("После каждого сканирования у вас будет возможность отсканировать следующую карту")
            
            cap = None  # Инициализируем переменную для камеры
            scan_count = 0
            
            while True:
                try:
                    # Если это первое сканирование или камера была закрыта, передаем None
                    # В противном случае используем сохраненную камеру
                    results, cap = reader.camera_capture_and_process(cap)
                    scan_count += 1
                    
                    print(f"\nРаспознанные данные (карта #{scan_count}):")
                    
                    # Вывод данных в понятном формате
                    if results['insurance_number']:
                        print(f"Страховой номер: {results['insurance_number']}")
                    else:
                        print("Страховой номер: Не распознан")
                        
                    # Фамилия - берем русский или белорусский вариант
                    surname = results['surname_ru'] or results['surname_be'] or "Не распознана"
                    print(f"Фамилия: {surname}")
                        
                    # Имя - берем русский или белорусский вариант
                    name = results['name_ru'] or results['name_be'] or "Не распознано"
                    print(f"Имя: {name}")
                        
                    # Отчество - берем русский или белорусский вариант
                    patronymic = results['patronymic_ru'] or results['patronymic_be'] or "Не распознано"
                    print(f"Отчество: {patronymic}")
                        
                    # Пол - берем русский или белорусский вариант
                    gender = results['gender_ru'] or results['gender_be'] or "Не распознан"
                    print(f"Пол: {gender}")
                        
                    if results['birth_date']:
                        print(f"Дата рождения: {results['birth_date']}")
                    else:
                        print("Дата рождения: Не распознана")
                    
                    # Пауза перед следующим сканированием
                    print("\nПауза 2 секунды перед следующим сканированием...")
                    time.sleep(2)
                    
                    print("\nГотов к сканированию следующей карты!")
                    print("Нажмите Enter для продолжения или введите 'выход' для завершения:")
                    user_input = input()
                    if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                        break
                        
                except ValueError as e:
                    if "Операция была отменена" in str(e):
                        break
                    else:
                        print(f"Ошибка: {str(e)}")
                        print("Попробуйте еще раз или введите 'выход' для завершения:")
                        user_input = input()
                        if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                            break
            
            # Закрываем камеру, если она открыта
            if cap is not None and cap.isOpened():
                cap.release()
                
            print(f"\nВсего отсканировано карт: {scan_count}")
            
        elif choice == '2':
            file_path = input("Введите путь к файлу изображения: ")
            results = reader.read_card(file_path)
            
            print("\nРаспознанные данные:")
            
            # Вывод данных в понятном формате
            if results['insurance_number']:
                print(f"Страховой номер: {results['insurance_number']}")
            else:
                print("Страховой номер: Не распознан")
                
            # Фамилия - берем русский или белорусский вариант
            surname = results['surname_ru'] or results['surname_be'] or "Не распознана"
            print(f"Фамилия: {surname}")
                
            # Имя - берем русский или белорусский вариант
            name = results['name_ru'] or results['name_be'] or "Не распознано"
            print(f"Имя: {name}")
                
            # Отчество - берем русский или белорусский вариант
            patronymic = results['patronymic_ru'] or results['patronymic_be'] or "Не распознано"
            print(f"Отчество: {patronymic}")
                
            # Пол - берем русский или белорусский вариант
            gender = results['gender_ru'] or results['gender_be'] or "Не распознан"
            print(f"Пол: {gender}")
                
            if results['birth_date']:
                print(f"Дата рождения: {results['birth_date']}")
            else:
                print("Дата рождения: Не распознана")
                
            # Дополнительные данные для отладки (показываем все распознанные поля)
            print("\nПодробная информация (включая двуязычные поля):")
            for field, value in results.items():
                if value:
                    print(f"{field}: {value}")
        else:
            print("Некорректный выбор")
            return
                
    except Exception as e:
        print(f"Ошибка при обработке изображения: {str(e)}")

if __name__ == "__main__":
    main() 