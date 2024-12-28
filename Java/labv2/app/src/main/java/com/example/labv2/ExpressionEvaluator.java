// src/main/java/com/example/labv2/ExpressionEvaluator.java
package com.example.labv2;
import java.util.*;

public class ExpressionEvaluator {
    public static double evaluate(String expr) {
        return evaluatePostfix(toPostfix(expr));
    }

    private static Map<String,Integer> precedence = new HashMap<>();
    static {
        precedence.put("+",1);
        precedence.put("-",1);
        precedence.put("*",2);
        precedence.put("/",2);
        precedence.put("^",3);
        precedence.put("%",2);
    }

    private static boolean isOperator(String s) {
        return precedence.containsKey(s) || s.equals("!");
    }

    private static boolean isFunction(String s) {
        return s.equals("sin")||s.equals("cos")||s.equals("ln")||s.equals("sqrt");
    }

    private static boolean isNumber(String s) {
        try { Double.parseDouble(s); return true; } catch(Exception e){return false;}
    }

    private static List<String> tokenize(String expr) {
        expr = expr.replaceAll(" ","");
        List<String> tokens = new ArrayList<>();
        StringBuilder num = new StringBuilder();
        for (int i=0;i<expr.length();i++){
            char c=expr.charAt(i);
            if ((c>='0' && c<='9')|| c=='.') {
                num.append(c);
            } else {
                if(num.length()>0) {
                    tokens.add(num.toString());
                    num=new StringBuilder();
                }
                if (c=='(' || c==')' || c=='+'||c=='-'||c=='*'||c=='/'||c=='^'||c=='%'||c=='!') {
                    tokens.add(String.valueOf(c));
                } else {
                    // function name
                    if (Character.isLetter(c)) {
                        StringBuilder func = new StringBuilder();
                        func.append(c);
                        while(i+1<expr.length() && Character.isLetter(expr.charAt(i+1))) {
                            i++;
                            func.append(expr.charAt(i));
                        }
                        tokens.add(func.toString());
                    }
                }
            }
        }
        if(num.length()>0) tokens.add(num.toString());
        return tokens;
    }

    private static List<String> toPostfix(String expr) {
        List<String> tokens = tokenize(expr);
        Stack<String> stack = new Stack<>();
        List<String> output = new ArrayList<>();
        for (String t : tokens) {
            if (isNumber(t)) {
                output.add(t);
            } else if (isFunction(t)) {
                stack.push(t);
            } else if (isOperator(t)) {
                if (t.equals("-") && (output.isEmpty() && stack.isEmpty() || (!output.isEmpty() && isOperator(output.get(output.size()-1))) || (!stack.isEmpty() && stack.peek().equals("(")))) {
                    // unary minus
                    output.add("0");
                }
                while(!stack.isEmpty() && !stack.peek().equals("(") && ( ( !t.equals("^") && precedenceCheck(stack.peek(),t)) || (t.equals("^") && !precedenceCheck(stack.peek(),t)) )) {
                    output.add(stack.pop());
                }
                stack.push(t);
            } else if (t.equals("(")) {
                stack.push(t);
            } else if (t.equals(")")) {
                while(!stack.isEmpty() && !stack.peek().equals("(")) {
                    output.add(stack.pop());
                }
                if(!stack.isEmpty()) stack.pop();
                if(!stack.isEmpty() && isFunction(stack.peek())) {
                    output.add(stack.pop());
                }
            }
        }
        while(!stack.isEmpty()) output.add(stack.pop());
        return output;
    }

    private static boolean precedenceCheck(String op1,String op2){
        return (precedence.containsKey(op1) && precedence.containsKey(op2) && precedence.get(op1)>=precedence.get(op2));
    }

    private static double fact(double x) {
        if (x<0) throw new IllegalArgumentException("Факториал не определен для отрицательных чисел");
        double r=1;
        int n=(int)x;
        for(int i=1;i<=n;i++) r*=i;
        return r;
    }

    private static double evaluatePostfix(List<String> postfix) {
        Stack<Double> stack = new Stack<>();
        for(String t: postfix) {
            if(isNumber(t)) {
                stack.push(Double.parseDouble(t));
            } else if (isOperator(t)) {
                double b = stack.pop();
                double a = stack.isEmpty()?0:stack.pop();
                double r=0;
                switch(t) {
                    case "+":r=a+b;break;
                    case "-":r=a-b;break;
                    case "*":r=a*b;break;
                    case "/":
                        if (b==0) throw new ArithmeticException("Деление на ноль");
                        r=a/b;break;
                    case "^":r=Math.pow(a,b);break;
                    case "%":
                        if (b==0) throw new ArithmeticException("Деление на ноль");
                        r=a%b;break;
                    case "!":
                        // ! applies to a single operand (b)
                        stack.push(a);
                        r=fact(b);
                        break;
                }
                stack.push(r);
            } else if (isFunction(t)) {
                double x= stack.pop();
                double r=0;
                switch(t) {
                    case "sin":r=Math.sin(x);break;
                    case "cos":r=Math.cos(x);break;
                    case "ln":
                        if(x<=0) throw new IllegalArgumentException("ln от неположительного числа");
                        r=Math.log(x);break;
                    case "sqrt":
                        if(x<0) throw new IllegalArgumentException("sqrt от отрицательного числа");
                        r=Math.sqrt(x);break;
                }
                stack.push(r);
            }
        }
        double val=stack.pop();
        if(!stack.isEmpty()) throw new IllegalArgumentException("Неверный ввод");
        if(Double.isInfinite(val)||Double.isNaN(val)) throw new ArithmeticException("Некорректный результат");
        return val;
    }
}
