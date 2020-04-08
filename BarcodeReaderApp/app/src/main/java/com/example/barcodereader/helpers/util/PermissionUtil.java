package com.example.barcodereader.helpers.util;

import android.app.Activity;
import android.content.pm.PackageManager;
import android.os.Build;

import androidx.fragment.app.Fragment;

import com.example.barcodereader.AppScanner;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class PermissionUtil {

    public static final int DEFAULT_PERM = 1;
    private static PermissionUtil _instance;

    private PermissionUtil() {}

    public static PermissionUtil on() {
        if (_instance == null) {
            _instance = new PermissionUtil();
        }
        return _instance;
    }

    public synchronized boolean requestPermission(Activity activity, String... permissions) {
        return requestPermission(null, activity, DEFAULT_PERM, Arrays.asList(permissions));
    }

    public synchronized boolean requestPermission(Fragment fragment, String... permissions) {
        return requestPermission(fragment, null, DEFAULT_PERM, Arrays.asList(permissions));
    }

    public synchronized boolean requestPermission(Activity activity, int requestCode, String... permissions) {
        return requestPermission(null, activity, requestCode, Arrays.asList(permissions));
    }

    public synchronized boolean requestPermission(Fragment fragment, int requestCode, String... permissions) {
        return requestPermission(fragment, null, requestCode, Arrays.asList(permissions));
    }

    private boolean requestPermission(Fragment fragment, Activity activity, int requestCode, List<String> permissions) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M)
            return true;

        List<String> permissionsNotTaken = new ArrayList<>();

        for (int i = 0; i < permissions.size(); i++) {
            if (!isAllowed(permissions.get(i)))
                permissionsNotTaken.add(permissions.get(i));
        }
        if (permissionsNotTaken.isEmpty())
            return true;

        if (fragment == null)
            activity.requestPermissions(permissionsNotTaken.toArray(
                    new String[permissionsNotTaken.size()]), requestCode
            );
        else
            fragment.requestPermissions(permissionsNotTaken.toArray(
                    new String[permissionsNotTaken.size()]), requestCode
            );
        return false;
    }

    boolean isAllowed(String permission) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M)
            return true;
        return AppScanner.getContext().checkSelfPermission(permission) == PackageManager.PERMISSION_GRANTED;
    }
}
