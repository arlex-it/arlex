package com.example.barcodereader;

import android.content.Context;

import androidx.multidex.MultiDex;
import androidx.multidex.MultiDexApplication;

import com.example.barcodereader.helpers.util.SharedPrefUtil;
import com.example.barcodereader.helpers.util.database.DatabaseUtil;
import com.google.android.gms.ads.MobileAds;

public class AppScanner extends MultiDexApplication {

    private static AppScanner _instance;

    public static Context getContext() {
        return _instance.getApplicationContext();
    }

    @Override
    protected void attachBaseContext(Context base) {
        super.attachBaseContext(base);
        MultiDex.install(this);
    }

    @Override
    public void onCreate() {
        super.onCreate();
        _instance = this;
        SharedPrefUtil.init(getApplicationContext());
        DatabaseUtil.init(getApplicationContext());
        MobileAds.initialize(this, getString(R.string.admob_app_id));
    }
}
