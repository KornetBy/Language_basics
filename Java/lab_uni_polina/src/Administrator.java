// Класс для администратора
public class Administrator {
    public void blockCreditCard(CreditCard creditCard) {
        if (creditCard.getCreditLimit() < creditCard.getDebt()) {
            creditCard.setBlocked(true);
            System.out.println("Кредитная карта заблокирована администратором за превышение кредита.");
        } else {
            System.out.println("Кредитный лимит не превышен. Карта не будет заблокирована.");
        }
    }
}
