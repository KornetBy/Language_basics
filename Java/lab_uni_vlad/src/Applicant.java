import java.util.ArrayList;
import java.util.List;

public class Applicant {
    private String name;
    private String faculty;
    private List<Exam> exams;
    private double averageGrade;

    public Applicant(String name, String faculty) {
        this.name = name;
        this.faculty = faculty;
        this.exams = new ArrayList<>();
    }

    public void addExam(Exam exam) {
        this.exams.add(exam);
    }

    public double calculateAverageGrade() {
        double total = 0;
        for (Exam exam : exams) {
            total += exam.getGrade();
        }
        this.averageGrade = total / exams.size();
        return this.averageGrade;
    }

    public String getName() {
        return name;
    }

    public String getFaculty() {
        return faculty;
    }

    public double getAverageGrade() {
        return averageGrade;
    }
}
