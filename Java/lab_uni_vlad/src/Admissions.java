import java.util.ArrayList;
import java.util.List;

public class Admissions {
    private List<Applicant> applicants;
    private double passingGrade;

    public Admissions(double passingGrade) {
        this.applicants = new ArrayList<>();
        this.passingGrade = passingGrade;
    }

    public void addApplicant(Applicant applicant) {
        applicants.add(applicant);
    }

    public List<Applicant> getAdmittedApplicants() {
        List<Applicant> admittedApplicants = new ArrayList<>();
        for (Applicant applicant : applicants) {
            if (applicant.calculateAverageGrade() >= passingGrade) {
                admittedApplicants.add(applicant);
            }
        }
        return admittedApplicants;
    }
}
