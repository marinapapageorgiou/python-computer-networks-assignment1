import java.net.Socket;
import java.net.ServerSocket;
import java.io.InputStream;
import java.io.OutputStream;

public class SimpleServer {

    public static void main(String [] args) throws Exception {

	int port = 4567;

	switch (args.length) {
	case 1: port = Integer.parseInt(args[0]);
	case 0: break;
	default:
	    System.err.println("Usage: SimpleServer [port (default=4567)]");
	    System.exit(1);
	}

	ServerSocket serv = new ServerSocket(port);
	int b;
	while (true) {
	    Socket s = serv.accept();
	    System.out.println("Connection from " + s.getInetAddress());
	    InputStream s_input = s.getInputStream();
	    OutputStream s_output = s.getOutputStream();

	    boolean connected = true;
	    while (connected) {
		System.out.print("other says: ");
		do {
		    b = s_input.read();
		    if (b == -1 ) { // end-of-input from socket => we close this connection 
			connected = false;
		    } else {
			System.out.write(b);
		    }
		} while (b != '\n' && connected);
		System.out.flush();

		if (!connected) 
		    break;

		System.out.print("you say> ");
		do {
		    b = System.in.read();
		    if (b == -1 ) { // end-of-input => we exit
			s.close();
			serv.close();
			System.exit(0);
		    }
		    s_output.write(b);
		} while (b != '\n');
		s_output.flush();
	    }
	    System.out.println("Connection with " + s.getInetAddress() + " is now closed.");
	    s.close();
	}
    }
}
