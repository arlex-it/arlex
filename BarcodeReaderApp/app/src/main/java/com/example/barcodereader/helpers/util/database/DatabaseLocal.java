package com.example.barcodereader.helpers.util.database;

import android.content.Context;

import androidx.room.Database;

import com.example.barcodereader.R;
import com.example.barcodereader.helpers.model.Code;
import com.example.barcodereader.helpers.model.CodeDAO;

@Database(entities = {Code.class}, version = 1, exportSchema = false)
public abstract class DatabaseLocal extends AppDatabase {

    private static volatile DatabaseLocal _instance;

    public static synchronized DatabaseLocal on() { return _instance; }

    public static synchronized void init(Context context) {
        if (_instance == null) {
            synchronized (DatabaseLocal.class) {
                _instance = createDb(context, context.getString(R.string.app_name));
            }
        }
    }

    public abstract CodeDAO codeDao();

}
