public class Notificador {

    public void enviar(String tipo, String mensaje) {

        if(tipo.equals("EMAIL")) {
            System.out.println("Enviando email: " + mensaje);
        }

        if(tipo.equals("SMS")) {
            System.out.println("Enviando SMS: " + mensaje);
        }

        if(tipo.equals("WHATSAPP")) {
            System.out.println("Enviando WhatsApp: " + mensaje);
        }

    }

}