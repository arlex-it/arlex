package com.example.barcodereader.helpers.util.database;

import android.os.Parcelable;

import androidx.annotation.NonNull;
import androidx.room.ColumnInfo;
import androidx.room.PrimaryKey;

import com.example.barcodereader.helpers.constant.ColumnNames;

public abstract class BaseEntity implements Parcelable {

    @PrimaryKey (autoGenerate = true)
    @ColumnInfo (name = ColumnNames.ID)
    @NonNull
    public long _id;

    public long getId() {
        return _id;
    }
}
