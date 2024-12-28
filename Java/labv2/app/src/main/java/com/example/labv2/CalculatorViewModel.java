// src/main/java/com/example/labv2/CalculatorViewModel.java
package com.example.labv2;

import androidx.lifecycle.ViewModel;
import java.util.ArrayList;
import java.util.List;

public class CalculatorViewModel extends ViewModel {
    private String expression = "";
    private String result = "0";
    private List<String> history = new ArrayList<>();

    public String getExpression() {
        return expression;
    }

    public void setExpression(String expr) {
        this.expression = expr;
    }

    public String getResult() {
        return result;
    }

    public void setResult(String res) {
        this.result = res;
    }

    public List<String> getHistory() {
        return history;
    }

    public void addHistory(String entry) {
        history.add(entry);
    }
}
