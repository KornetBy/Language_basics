// Главный класс для тестирования системы
public class PaymentSystem {
    public static void main(String[] args) {
        Account account1 = new Account(1000);
        CreditCard creditCard1 = new CreditCard(500);
        Client client = new Client("Иван", account1, creditCard1);

        Administrator admin = new Administrator();

        client.makePayment(200); // Клиент оплачивает заказ
        client.transferToAccount(new Account(300), 150); // Перевод на другой счет
        client.blockCreditCard(); // Клиент блокирует карту
        client.closeAccount(); // Клиент аннулирует счет

        admin.blockCreditCard(client.getCreditCard()); // Администратор блокирует карту за превышение
    }
}

