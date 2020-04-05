package com.example.barcodereader.helpers.model;

import android.os.Parcel;
import android.os.Parcelable;

import androidx.room.Entity;

import com.example.barcodereader.helpers.constant.TableNames;
import com.example.barcodereader.helpers.util.database.BaseEntity;

@Entity(tableName = TableNames.CODES)
public class Code extends BaseEntity {

    public static final int QR_CODE = 1;
    public static final int BAR_CODE = 2;

    public static final Parcelable.Creator<Code> CREATOR = new Parcelable.Creator<Code>() {
        @Override
        public Code createFromParcel(Parcel source) {
            return new Code(source);
        }

        @Override
        public Code[] newArray(int size) {
            return new Code[size];
        }
    };

    private String _content;
    private String _imagePath;
    private long _timestamp;
    private int _type;

    public Code() {}

    public Code(String content, int type) {
        this._content = content;
        this._type = type;
    }

    public Code(String content, int type, long timestamp) {
        this._content = content;
        this._type = type;
        this._timestamp = timestamp;
    }

    public Code(String content, int type, String imagePath, long timestamp) {
        this._content = content;
        this._type = type;
        this._timestamp = timestamp;
        this._imagePath = imagePath;
    }

    public Code(Parcel source) {
        /*this.mContent = getmContent();
        this.mType = getmType();
        this.mTimeStamp = getmTimeStamp();
        this.mCodeImagePath = getmCodeImagePath();*/
    }


    public String getContent() {
        return _content;
    }

    public void setContent(String content) {
        this._content = content;
    }

    public int getType() {
        return _type;
    }

    public void setType(int type) {
        this._type = type;
    }

    public String getImagePath() {
        return _imagePath;
    }

    public void setImagePath(String imagePath) {
        this._imagePath = imagePath;
    }

    public long getTimestamp() {
        return _timestamp;
    }

    public void setTimestamp(long timestamp) {
        this._timestamp = timestamp;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(this._content);
        dest.writeInt(this._type);
        dest.writeLong(this._timestamp);
        dest.writeString(this._imagePath);
    }
}
