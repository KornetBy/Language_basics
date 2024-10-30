import java.util.List;

public class Main {
    public static void main(String[] args) {
        // Регистрация абитуриентов
        Applicant applicant1 = new Applicant("Иван Иванов", "Факультет Математики");
        Applicant applicant2 = new Applicant("Анна Петрова", "Факультет Информатики");

        // Создание преподавателей
        Teacher teacher1 = new Teacher("Преподаватель 1");
        Teacher teacher2 = new Teacher("Преподаватель 2");

        // Выставление оценок
        teacher1.setGrade(applicant1, "Математика", 85);
        teacher2.setGrade(applicant1, "Физика", 90);

        teacher1.setGrade(applicant2, "Математика", 75);
        teacher2.setGrade(applicant2, "Физика", 70);

        // Создание процесса зачисления с проходным баллом 80
        Admissions admissions = new Admissions(80);
        admissions.addApplicant(applicant1);
        admissions.addApplicant(applicant2);

        // Определение зачисленных абитуриентов
        List<Applicant> admittedApplicants = admissions.getAdmittedApplicants();
        System.out.println("Зачисленные абитуриенты:");
        for (Applicant admitted : admittedApplicants) {
            System.out.println(admitted.getName() + " с факультета " + admitted.getFaculty() + " со средним баллом " + admitted.getAverageGrade());
        }

        // Вывод данных о преподавателях
        System.out.println("\nДанные о преподавателях:");
        teacher1.printGrades();
        teacher2.printGrades();
    }
}
