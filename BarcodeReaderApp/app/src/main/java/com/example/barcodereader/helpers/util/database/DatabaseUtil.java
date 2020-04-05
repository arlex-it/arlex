package com.example.barcodereader.helpers.util.database;

import android.content.Context;

import com.example.barcodereader.helpers.model.Code;
import com.example.barcodereader.helpers.model.CodeDAO;

import java.util.List;

import io.reactivex.Completable;
import io.reactivex.Flowable;

public class DatabaseUtil {
    private static DatabaseUtil _instance;
    private CodeDAO _codeDAO;

    private DatabaseUtil() { setCodeDao(QrDatabase.on().codeDao()); }

    public static void init(Context context) {
        QrDatabase.init(context);

        if (_instance == null) {
            _instance = new DatabaseUtil();
        }
    }

    public static DatabaseUtil on() {
        if (_instance == null) {
            _instance = new DatabaseUtil();
        }
        return _instance;
    }

    private CodeDAO getCodeDao() { return _codeDAO; }

    private void setCodeDao(CodeDAO codeDAO) { this._codeDAO = codeDAO; }

    public Completable insertCode(Code code) { return getCodeDao().insert(code); }

    public Flowable<List<Code>> getAllCodes() { return getCodeDao().getAllFlowableCodes(); }
    public int deleteEntity(Code code) { return getCodeDao().delete(code); }
}
