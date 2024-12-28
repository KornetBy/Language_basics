package com.example.lab22;

import android.app.AlertDialog;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.LinkedList;

public class MainActivity extends AppCompatActivity {

    private TextView inputTextView;
    private TextView resultTextView;

    private String currentExpression = "";
    private String currentResult = "";

    private Double memory = null;
    private ExpressionEvaluator evaluator = new ExpressionEvaluator();

    // История вычислений (хранит последние 10)
    private LinkedList<String> historyList = new LinkedList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Предполагается, что при смене ориентации подбирается нужный макет.
        setContentView(R.layout.activity_main);

        inputTextView = findViewById(R.id.inputTextView);
        resultTextView = findViewById(R.id.resultTextView);

        if (savedInstanceState != null) {
            currentExpression = savedInstanceState.getString("EXPRESSION_STATE", "");
            currentResult = savedInstanceState.getString("RESULT_STATE", "");
            ArrayList<String> savedHistory = savedInstanceState.getStringArrayList("HISTORY_STATE");
            if (savedHistory != null) {
                historyList.clear();
                historyList.addAll(savedHistory);
            }
            String memVal = savedInstanceState.getString("MEMORY_STATE");
            if (memVal != null) {
                memory = Double.valueOf(memVal);
            }
            updateDisplay();
        }

        // Цифры
        int[] digits = {
                R.id.btn0, R.id.btn1, R.id.btn2, R.id.btn3, R.id.btn4,
                R.id.btn5, R.id.btn6, R.id.btn7, R.id.btn8, R.id.btn9
        };
        for (int id : digits) {
            Button btn = findViewById(id);
            if (btn != null) {
                btn.setOnClickListener(v -> appendToExpression(btn.getText().toString()));
            }
        }

        // Операции: + - * / %
        int[] ops = {
                R.id.btnPlus, R.id.btnMinus, R.id.btnMultiply, R.id.btnDivide, R.id.btnPercent
        };
        for (int id : ops) {
            Button btn = findViewById(id);
            if (btn != null) {
                btn.setOnClickListener(v -> appendToExpression(btn.getText().toString()));
            }
        }

        // Дополнительные: . ( ) ^ √ ! π
        int[] extraOps = {
                R.id.btnDot, R.id.btnOpenParen, R.id.btnCloseParen,
                R.id.btnPower, R.id.btnSqrt, R.id.btnFactorial, R.id.btnPi
        };
        for (int id : extraOps) {
            Button btn = findViewById(id);
            if (btn != null) {
                btn.setOnClickListener(v -> appendToExpression(btn.getText().toString()));
            }
        }

        // Тригонометрия и логарифмы: sin, cos, tg, ln, log
        int[] trigOps = {
                R.id.btnSin, R.id.btnCos, R.id.btnTg, R.id.btnLn, R.id.btnLog
        };
        for (int id : trigOps) {
            Button btn = findViewById(id);
            if (btn != null) {
                btn.setOnClickListener(v -> {
                    String func = btn.getText().toString().toLowerCase() + "(";
                    appendToExpression(func);
                });
            }
        }

        // Кнопка очистки
        Button acButton = findViewById(R.id.btnAC);
        if (acButton != null) {
            acButton.setOnClickListener(v -> {
                currentExpression = "";
                currentResult = "";
                updateDisplay();
            });
        }

        // Кнопка backspace
        Button backspaceButton = findViewById(R.id.btnBackspace);
        if (backspaceButton != null) {
            backspaceButton.setOnClickListener(v -> {
                if (!currentExpression.isEmpty()) {
                    currentExpression = currentExpression.substring(0, currentExpression.length() - 1);
                    updateDisplay();
                }
            });
        }

        // Кнопка равно
        Button equalsButton = findViewById(R.id.btnEquals);
        if (equalsButton != null) {
            equalsButton.setOnClickListener(v -> calculateResult());
        }

        // Кнопка истории
        Button historyButton = findViewById(R.id.btnHistory);
        if (historyButton != null) {
            historyButton.setOnClickListener(v -> showHistoryDialog());
        }

        // Кнопки памяти: MC, MR, M+, M-
        Button mcButton = findViewById(R.id.btnMC);
        if (mcButton != null) {
            mcButton.setOnClickListener(v -> memory = null);
        }

        Button mrButton = findViewById(R.id.btnMR);
        if (mrButton != null) {
            mrButton.setOnClickListener(v -> {
                if (memory != null) {
                    appendToExpression(memory.toString());
                }
            });
        }

        Button mPlusButton = findViewById(R.id.btnMPlus);
        if (mPlusButton != null) {
            mPlusButton.setOnClickListener(v -> {
                if (!currentResult.isEmpty() && !currentResult.equals("Ошибка")) {
                    double value = Double.parseDouble(currentResult);
                    if (memory == null) {
                        memory = value;
                    } else {
                        memory = memory + value;
                    }
                }
            });
        }

        Button mMinusButton = findViewById(R.id.btnMMinus);
        if (mMinusButton != null) {
            mMinusButton.setOnClickListener(v -> {
                if (!currentResult.isEmpty() && !currentResult.equals("Ошибка")) {
                    double value = Double.parseDouble(currentResult);
                    if (memory == null) {
                        memory = -value;
                    } else {
                        memory = memory - value;
                    }
                }
            });
        }
    }

    private void calculateResult() {
        try {
            double res = evaluator.evaluate(currentExpression);
            currentResult = Double.toString(res);
            addToHistory(currentExpression + " = " + currentResult);
        } catch (ArithmeticException ae) {
            currentResult = "Ошибка: " + ae.getMessage();
        } catch (IllegalArgumentException ie) {
            currentResult = "Ошибка: " + ie.getMessage();
        } catch (Exception e) {
            currentResult = "Ошибка: Некорректный ввод";
        }
        updateDisplay();
    }

    private void addToHistory(String entry) {
        historyList.addFirst(entry);
        if (historyList.size() > 10) {
            historyList.removeLast();
        }
    }

    private void showHistoryDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("История вычислений");

        if (historyList.isEmpty()) {
            builder.setMessage("История пуста");
            builder.setPositiveButton("OK", null);
        } else {
            String[] arr = historyList.toArray(new String[0]);
            builder.setItems(arr, null);
            builder.setPositiveButton("OK", null);
        }

        builder.create().show();
    }

    private void appendToExpression(String str) {
        currentExpression += str;
        updateDisplay();
    }

    private void updateDisplay() {
        inputTextView.setText(currentExpression);
        resultTextView.setText(currentResult);
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putString("EXPRESSION_STATE", currentExpression);
        outState.putString("RESULT_STATE", currentResult);
        ArrayList<String> histArr = new ArrayList<>(historyList);
        outState.putStringArrayList("HISTORY_STATE", histArr);
        if (memory != null) {
            outState.putString("MEMORY_STATE", memory.toString());
        }
    }
}
