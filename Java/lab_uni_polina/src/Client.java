// Класс для клиента
public class Client {
    private String name;
    private Account account;
    private CreditCard creditCard;

    public Client(String name, Account account, CreditCard creditCard) {
        this.name = name;
        this.account = account;
        this.creditCard = creditCard;
    }

    public void makePayment(double amount) {
        if (creditCard.isBlocked()) {
            System.out.println("Кредитная карта заблокирована. Оплата невозможна.");
            return;
        }
        account.withdraw(amount);
        System.out.println("Оплата в размере " + amount + " выполнена.");
    }

    public void transferToAccount(Account targetAccount, double amount) {
        if (creditCard.isBlocked()) {
            System.out.println("Кредитная карта заблокирована. Перевод невозможен.");
            return;
        }
        account.withdraw(amount);
        targetAccount.deposit(amount);
        System.out.println("Перевод в размере " + amount + " выполнен.");
    }

    public void blockCreditCard() {
        creditCard.setBlocked(true);
        System.out.println("Кредитная карта заблокирована.");
    }

    public void closeAccount() {
        account.setClosed(true);
        System.out.println("Счет аннулирован.");
    }

    public Account getAccount() {
        return account;
    }

    public CreditCard getCreditCard() {
        return creditCard;
    }
}
