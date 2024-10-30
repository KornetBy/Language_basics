// Класс для счета
public class Account {
    private double balance;
    private boolean isClosed;

    public Account(double balance) {
        this.balance = balance;
        this.isClosed = false;
    }

    public void deposit(double amount) {
        if (!isClosed) {
            balance += amount;
            System.out.println("Счет пополнен на " + amount + ". Баланс: " + balance);
        } else {
            System.out.println("Счет аннулирован. Пополнение невозможно.");
        }
    }

    public void withdraw(double amount) {
        if (!isClosed && balance >= amount) {
            balance -= amount;
            System.out.println("Снятие со счета на " + amount + ". Баланс: " + balance);
        } else {
            System.out.println("Недостаточно средств или счет аннулирован.");
        }
    }

    public double getBalance() {
        return balance;
    }

    public boolean isClosed() {
        return isClosed;
    }

    public void setClosed(boolean closed) {
        this.isClosed = closed;
    }
}
