package com.example.barcodereader.helpers.util;

import com.example.barcodereader.helpers.constant.AppConstants;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Locale;

public class TimeUtil {

    public static String getFormattedDateString(long ms) {
        Calendar calendar = Calendar.getInstance();
        calendar.setTimeInMillis(ms);
        return new SimpleDateFormat(AppConstants.APP_COMMON_DATE_FORMAT, Locale.ENGLISH).format(calendar.getTime());
    }

    public static String getFormattedDateString(long milliseconds, String format) {
        Calendar calendar = Calendar.getInstance();
        calendar.setTimeInMillis(milliseconds);
        return new SimpleDateFormat(format, Locale.ENGLISH).format(calendar.getTime());
    }

}
