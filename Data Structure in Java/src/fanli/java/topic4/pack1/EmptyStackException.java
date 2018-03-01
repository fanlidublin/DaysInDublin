package fanli.java.topic4.pack1;
/**
 * Runtime exception thrown when one tries to perform operation top or
 * pop on an empty stack.
 */

public class EmptyStackException extends RuntimeException {  
  public EmptyStackException(String err) {
    super(err);
  }
}
