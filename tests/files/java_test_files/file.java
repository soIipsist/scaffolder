public class File {
    
    // Public method with no parameters
    public void publicMethod() {
        System.out.println("This is a public method.");
    }
    
    // Protected method with parameters
    protected int protectedMethod(int x, int y) {
        return x + y;
    }
    
    // Private method with parameters
    private String privateMethod(String input) {
        return "Hello, " + input;
    }
    
    // Static method
    public static void staticMethod() {
        System.out.println("This is a static method.");
    }
    
    // Final method
    public final void finalMethod() {
        System.out.println("This is a final method.");
    }
    
    // Synchronized method
    public synchronized void synchronizedMethod() {
        System.out.println("This is a synchronized method.");
    }
    
    // Native method (note: native methods are usually declared in interfaces or abstract classes)
    public native void nativeMethod();
    
    // Abstract method in an abstract class
    abstract class AbstractClass {
        public abstract void abstractMethod();
    }
    
    // Transient and volatile are not applicable to methods, only to variables.
    // Example of a method with an annotation
    @Deprecated
    public void deprecatedMethod() {
        System.out.println("This method is deprecated.");
    }

    // Method with a generic type
    public <T> T genericMethod(T input) {
        return input;
    }
    
    // Method with a throws clause
    public void methodWithException() throws Exception {
        throw new Exception("This method throws an exception.");
    }
    
    // Method with multiple modifiers
    private abstract static final synchronized void multipleModifiersMethod() {
        System.out.println("This method has multiple modifiers.");
    }

    abstract void hi(){
        
    }
}
