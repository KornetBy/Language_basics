import java.util.HashMap;
import java.util.Map;

public class Teacher {
    private String name;
    private Map<String, Map<String, Integer>> gradesGiven; // Абитуриент -> (Предмет -> Оценка)

    public Teacher(String name) {
        this.name = name;
        this.gradesGiven = new HashMap<>();
    }

    public String getName() {
        return name;
    }

    public void setGrade(Applicant applicant, String subject, int grade) {
        // Используем метод addExam вместо несуществующего addGrade
        Exam exam = new Exam(subject, grade);
        applicant.addExam(exam);

        gradesGiven.computeIfAbsent(applicant.getName(), k -> new HashMap<>()).put(subject, grade);
    }

    public Map<String, Map<String, Integer>> getGradesGiven() {
        return gradesGiven;
    }

    public void printGrades() {
        System.out.println("Преподаватель " + name + " выставил следующие оценки:");
        for (Map.Entry<String, Map<String, Integer>> entry : gradesGiven.entrySet()) {
            String applicantName = entry.getKey();
            Map<String, Integer> subjectGrades = entry.getValue();
            System.out.println("  Абитуриент: " + applicantName);
            for (Map.Entry<String, Integer> gradeEntry : subjectGrades.entrySet()) {
                System.out.println("    Предмет: " + gradeEntry.getKey() + ", Оценка: " + gradeEntry.getValue());
            }
        }
    }
}
