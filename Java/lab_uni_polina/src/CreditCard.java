// Класс для кредитной карты
public class CreditCard {
    private double creditLimit;
    private double debt;
    private boolean isBlocked;

    public CreditCard(double creditLimit) {
        this.creditLimit = creditLimit;
        this.debt = 0;
        this.isBlocked = false;
    }

    public void addDebt(double amount) {
        if (!isBlocked && debt + amount <= creditLimit) {
            debt += amount;
            System.out.println("Добавлен долг на сумму " + amount + ". Общий долг: " + debt);
        } else {
            System.out.println("Лимит превышен или карта заблокирована.");
        }
    }

    public double getCreditLimit() {
        return creditLimit;
    }

    public double getDebt() {
        return debt;
    }

    public boolean isBlocked() {
        return isBlocked;
    }

    public void setBlocked(boolean blocked) {
        this.isBlocked = blocked;
    }
}
