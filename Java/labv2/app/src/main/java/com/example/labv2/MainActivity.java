// src/main/java/com/example/labv2/MainActivity.java
package com.example.labv2;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private CalculatorViewModel viewModel;
    private TextView tvExpression;
    private TextView tvResult;
    private RecyclerView rvHistory;
    private HistoryAdapter historyAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        viewModel = new ViewModelProvider(this).get(CalculatorViewModel.class);

        tvExpression = findViewById(R.id.tvExpression);
        tvResult = findViewById(R.id.tvResult);
        Button btnEquals = findViewById(R.id.btnEquals);
        Button btnReset = findViewById(R.id.btnReset);

        if (findViewById(R.id.rvHistory) != null) {
            rvHistory = findViewById(R.id.rvHistory);
            historyAdapter = new HistoryAdapter(viewModel.getHistory());
            rvHistory.setLayoutManager(new LinearLayoutManager(this));
            rvHistory.setAdapter(historyAdapter);
        }

        tvExpression.setText(viewModel.getExpression());
        tvResult.setText(viewModel.getResult());

        int[] buttonIds = new int[]{
                R.id.btn0, R.id.btn1, R.id.btn2, R.id.btn3, R.id.btn4,
                R.id.btn5, R.id.btn6, R.id.btn7, R.id.btn8, R.id.btn9,
                R.id.btnAdd, R.id.btnSubtract, R.id.btnMultiply, R.id.btnDivide,
                R.id.btnDot, R.id.btnPercent, R.id.btnSin, R.id.btnCos,
                R.id.btnLn, R.id.btnFactorial
        };

        for (int id : buttonIds) {
            Button btn = findViewById(id);
            btn.setOnClickListener(v -> {
                String btnText = ((Button) v).getText().toString();
                appendToExpression(btnText);
            });
        }

        btnReset.setOnClickListener(v -> {
            viewModel.setExpression("");
            viewModel.setResult("0");
            tvExpression.setText("");
            tvResult.setText("0");
        });

        btnEquals.setOnClickListener(v -> {
            String expr = viewModel.getExpression();
            if (expr.isEmpty()) {
                Toast.makeText(this, "Выражение пустое", Toast.LENGTH_SHORT).show();
                return;
            }
            try {
                double result = ExpressionEvaluator.evaluate(expr);
                viewModel.setResult(String.valueOf(result));
                tvResult.setText(viewModel.getResult());
                viewModel.addHistory(expr + " = " + result);
                if (rvHistory != null) {
                    historyAdapter.notifyDataSetChanged();
                }
            } catch (ArithmeticException e) {
                viewModel.setResult("Ошибка: " + e.getMessage());
                tvResult.setText(viewModel.getResult());
            } catch (IllegalArgumentException e) {
                viewModel.setResult("Ошибка: " + e.getMessage());
                tvResult.setText(viewModel.getResult());
            } catch (Exception e) {
                viewModel.setResult("Ошибка: " + e.getMessage());
                tvResult.setText(viewModel.getResult());
            }
        });
    }

    private void appendToExpression(String str) {
        String currentExpr = viewModel.getExpression();
        currentExpr += str;
        viewModel.setExpression(currentExpr);
        tvExpression.setText(currentExpr);
    }
}
