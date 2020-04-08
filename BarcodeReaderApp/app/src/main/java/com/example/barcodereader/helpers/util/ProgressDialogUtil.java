package com.example.barcodereader.helpers.util;

import android.app.AlertDialog;
import android.content.Context;
import android.graphics.Typeface;
import android.view.LayoutInflater;

import com.example.barcodereader.databinding.ProgressDialogLayoutBinding;

public class ProgressDialogUtil {

    private static ProgressDialogUtil _instance;
    private AlertDialog _alertBox;

    private ProgressDialogUtil() {}

    public static ProgressDialogUtil on() {
        if (_instance == null)
            _instance = new ProgressDialogUtil();
        return _instance;
    }

    public void showProgressDialog(Context context) {
        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        ProgressDialogLayoutBinding binding = ProgressDialogLayoutBinding.inflate(LayoutInflater.from(context), null, false);

        binding.textViewMessage.setTypeface(null, Typeface.NORMAL);
        builder.setCancelable(false);
        builder.setView(binding.getRoot());

        _alertBox = builder.create();
        _alertBox.show();
    }

    public void hideProgressDialog() {
        if (_alertBox != null) {
            _alertBox.dismiss();
            _alertBox = null;
        }
    }

}
