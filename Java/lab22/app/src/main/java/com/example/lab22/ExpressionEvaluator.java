package com.example.lab22;

import java.util.regex.*;
import static java.lang.Math.*;

public class ExpressionEvaluator {

    public double evaluate(String expression) {
        String prepared = prepareExpression(expression);
        if (prepared.trim().isEmpty()) return 0.0;
        return parseExpression(prepared);
    }

    private String prepareExpression(String expr) {
        // Заменяем функции на упрощённые символы
        return expr
                .replace("sin(", "s(")
                .replace("cos(", "c(")
                .replace("tg(", "t(")
                .replace("ln(", "l(")
                .replace("log(", "g(")
                .replace("√", "q")
                .replace("π", Double.toString(Math.PI));
    }

    private double parseExpression(String expr) {
        String e = expr.replace(" ", "");
        return evaluateByPriority(e);
    }

    private double evaluateByPriority(String e) {
        // Сначала обработаем скобки
        if (e.contains("(")) {
            String expr = e;
            while (expr.contains("(")) {
                int closeIndex = expr.indexOf(')');
                if (closeIndex == -1) throw new IllegalArgumentException("Непарная скобка");
                int openIndex = expr.substring(0, closeIndex).lastIndexOf('(');
                if (openIndex == -1) throw new IllegalArgumentException("Непарная скобка");
                String inner = expr.substring(openIndex + 1, closeIndex);
                double innerVal = evaluateByPriority(inner);
                expr = expr.substring(0, openIndex) + innerVal + expr.substring(closeIndex + 1);
            }
            return evaluateByPriority(expr);
        }

        String expr = processFunctions(e);
        expr = processFactorial(expr);
        expr = processPower(expr);
        expr = processMultiplicationDivisionPercent(expr);
        return processAdditionSubtraction(expr);
    }

    private String processFunctions(String expr) {
        String e = expr;
        e = processUnaryFunction(e, 'q', val -> {
            if (val < 0) throw new IllegalArgumentException("Корень из отрицательного числа не определён");
            return sqrt(val);
        });
        e = processUnaryFunction(e, 's', val -> sin(val));
        e = processUnaryFunction(e, 'c', val -> cos(val));
        e = processUnaryFunction(e, 't', val -> tan(val));
        e = processUnaryFunction(e, 'l', val -> {
            if (val <= 0) throw new IllegalArgumentException("ln(x) определён только для x>0");
            return log(val);
        });
        e = processUnaryFunction(e, 'g', val -> {
            if (val <= 0) throw new IllegalArgumentException("log10(x) определён только для x>0");
            return log10(val);
        });
        return e;
    }

    private interface UnaryOp {
        double apply(double val);
    }

    private String processUnaryFunction(String expr, char funcChar, UnaryOp op) {
        String e = expr;
        while (true) {
            int index = e.indexOf(funcChar + "(");
            if (index == -1) break;
            int close = findClosingParenthesis(e, index + 2);
            String inner = e.substring(index + 2, close);
            double valInner = evaluateByPriority(inner);
            double res = op.apply(valInner);
            e = e.substring(0, index) + res + e.substring(close + 1);
        }
        return e;
    }

    private int findClosingParenthesis(String s, int start) {
        int count = 0;
        for (int i = start; i < s.length(); i++) {
            if (s.charAt(i) == '(') count++;
            if (s.charAt(i) == ')') {
                if (count == 0) return i;
                count--;
            }
        }
        throw new IllegalArgumentException("Непарная скобка");
    }

    private String processFactorial(String expr) {
        String e = expr;
        while (true) {
            int index = e.indexOf('!');
            if (index == -1) break;
            int startIndex = index - 1;
            while (startIndex >= 0 && (Character.isDigit(e.charAt(startIndex)) || e.charAt(startIndex) == '.')) {
                startIndex--;
            }
            String number = e.substring(startIndex + 1, index);
            double value = factorial(Double.parseDouble(number));
            e = e.substring(0, startIndex + 1) + value + e.substring(index + 1);
        }
        return e;
    }

    private double factorial(double num) {
        if (num < 0) throw new IllegalArgumentException("Факториал отрицательных чисел не определён");
        int n = (int) num;
        if (n != num) throw new IllegalArgumentException("Факториал определён только для целых чисел");
        double res = 1.0;
        for (int i = 1; i <= n; i++) {
            res *= i;
        }
        return res;
    }

    private String processPower(String expr) {
        String e = expr;
        while (true) {
            int index = e.indexOf('^');
            if (index == -1) break;
            double[] left = readNumberFromLeft(e, index - 1);
            double leftNumber = left[0];
            int leftStart = (int) left[1];
            double[] right = readNumberFromRight(e, index + 1);
            double rightNumber = right[0];
            int rightEnd = (int) right[1];
            double powerVal = Math.pow(leftNumber, rightNumber);
            e = e.substring(0, leftStart) + powerVal + e.substring(rightEnd + 1);
        }
        return e;
    }

    private String processMultiplicationDivisionPercent(String expr) {
        String e = expr;
        char[] ops = {'*', '/', '%'};
        while (true) {
            int index = findNextOperator(e, ops);
            if (index == -1) break;
            char op = e.charAt(index);
            double[] left = readNumberFromLeft(e, index - 1);
            double leftNumber = left[0];
            int leftStart = (int) left[1];
            double[] right = readNumberFromRight(e, index + 1);
            double rightNumber = right[0];
            int rightEnd = (int) right[1];
            double result;
            switch (op) {
                case '*':
                    result = leftNumber * rightNumber;
                    break;
                case '/':
                    if (rightNumber == 0.0) throw new ArithmeticException("Деление на ноль");
                    result = leftNumber / rightNumber;
                    break;
                case '%':
                    result = leftNumber * rightNumber / 100.0;
                    break;
                default:
                    result = 0.0;
            }
            e = e.substring(0, leftStart) + result + e.substring(rightEnd + 1);
        }
        return e;
    }

    private double processAdditionSubtraction(String expr) {
        String e = expr;
        if (e.isEmpty()) return 0.0;
        if (e.startsWith("-")) {
            e = "0" + e;
        }
        Pattern regex = Pattern.compile("(?=[+-])");
        String[] parts = regex.split(e);
        double sum = 0.0;
        for (String part : parts) {
            if (part.isEmpty()) continue;
            if (part.startsWith("+")) {
                sum += Double.parseDouble(part.substring(1));
            } else if (part.startsWith("-")) {
                sum -= Double.parseDouble(part.substring(1));
            } else {
                sum += Double.parseDouble(part);
            }
        }
        return sum;
    }

    private int findNextOperator(String expr, char[] ops) {
        for (int i = 0; i < expr.length(); i++) {
            char ch = expr.charAt(i);
            for (char op : ops) {
                if (ch == op) return i;
            }
        }
        return -1;
    }

    /**
     * Читает число слева от оператора, начиная с позиции start.
     * Возвращает массив {значение, индексНачалаЧисла}.
     */
    private double[] readNumberFromLeft(String expr, int start) {
        if (start < 0) return new double[]{0.0, -1};
        int i = start;
        while (i >= 0 && (Character.isDigit(expr.charAt(i)) || expr.charAt(i) == '.')) {
            i--;
        }
        String numStr = expr.substring(i + 1, start + 1);
        if (numStr.isEmpty()) throw new IllegalArgumentException("Некорректный ввод числа слева от оператора");
        return new double[]{Double.parseDouble(numStr), i + 1};
    }

    /**
     * Читает число справа от оператора, начиная с позиции start.
     * Возвращает массив {значение, индексКонцаЧисла}.
     */
    private double[] readNumberFromRight(String expr, int start) {
        int i = start;
        while (i < expr.length() && (Character.isDigit(expr.charAt(i)) || expr.charAt(i) == '.')) {
            i++;
        }
        String numStr = expr.substring(start, i);
        if (numStr.isEmpty()) throw new IllegalArgumentException("Некорректный ввод числа справа от оператора");
        return new double[]{Double.parseDouble(numStr), i - 1};
    }

}
