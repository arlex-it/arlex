package com.example.barcodereader.helpers.util.image;

import android.net.Uri;

public class ImageInfo {

    private Uri _imageUri;
    private boolean _takenByCamera;

    public ImageInfo() {}

    public ImageInfo(Uri imageUri, boolean takenByCamera) {
        _imageUri = imageUri;
        _takenByCamera = takenByCamera;
    }

    public Uri getImageUri() { return _imageUri; }

    public void setImageUri(Uri imageUri) { _imageUri = imageUri; }

    public boolean isTakenByCamera() { return _takenByCamera; }

    public void setTakenByCamera(boolean takenByCamera) { _takenByCamera = takenByCamera; }

}
