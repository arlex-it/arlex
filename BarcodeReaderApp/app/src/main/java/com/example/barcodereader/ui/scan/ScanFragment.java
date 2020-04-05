package com.example.barcodereader.ui.scan;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.text.TextUtils;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.content.ContextCompat;
import androidx.loader.content.CursorLoader;

import com.example.barcodereader.R;
import com.example.barcodereader.helpers.constant.AppConstants;
import com.example.barcodereader.helpers.constant.IntentKey;
import com.example.barcodereader.helpers.constant.PreferenceKey;
import com.example.barcodereader.helpers.model.Code;
import com.example.barcodereader.helpers.util.FileUtil;
import com.example.barcodereader.helpers.util.ProgressDialogUtil;
import com.example.barcodereader.helpers.util.SharedPrefUtil;
import com.example.barcodereader.helpers.util.image.ImageInfo;
import com.example.barcodereader.helpers.util.image.ImagePicker;
import com.example.barcodereader.ui.pickedfromgallery.PickedFromGalleryActivity;
import com.example.barcodereader.ui.scanresult.ScanResultActivity;
import com.google.zxing.BinaryBitmap;
import com.google.zxing.DecodeHintType;
import com.google.zxing.LuminanceSource;
import com.google.zxing.MultiFormatReader;
import com.google.zxing.RGBLuminanceSource;
import com.google.zxing.Reader;
import com.google.zxing.Result;
import com.google.zxing.ResultPoint;
import com.google.zxing.client.android.BeepManager;
import com.google.zxing.common.HybridBinarizer;
import com.journeyapps.barcodescanner.BarcodeCallback;
import com.journeyapps.barcodescanner.BarcodeResult;
import com.journeyapps.barcodescanner.DecoratedBarcodeView;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Hashtable;
import java.util.List;
import java.util.Locale;
import java.util.Objects;

public class ScanFragment extends androidx.fragment.app.Fragment implements View.OnClickListener {

    private Context _context;
    private Activity _activity;
    private DecoratedBarcodeView _barcodeView;
    private BeepManager _beepManager;
    private TextView _textViewFlash, _textViewScanGallery;
    private boolean _isFlashOn;

    public ScanFragment() {}

    public static ScanFragment newInstance() {
        return new ScanFragment();
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        _context = context;
    }

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_scan, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        if (getActivity() == null) {
            return;
        } else {
            _activity = getActivity();
        }

        initializeViews(view);
        doPreRequisites();
        setListeners();
        doScan();
    }

    private void doScan() {
        _barcodeView.decodeSingle(new BarcodeCallback() {
            @Override
            public void barcodeResult(BarcodeResult result) {
                _barcodeView.pause();
                _beepManager.playBeepSoundAndVibrate();

                if (result != null && !TextUtils.isEmpty(result.getText())
                                    && !TextUtils.isEmpty(result.getBarcodeFormat().name())) {
                    Code code;

                    if (result.getBitmap() != null) {
                        int typeIndex = result.getBarcodeFormat().name().toLowerCase().startsWith("qr") ? Code.QR_CODE : Code.BAR_CODE;
                        String type = getResources().getStringArray(R.array.code_types)[typeIndex];

                        File codeImageFile = FileUtil.getEmptyFile(_context, AppConstants.PREFIX_IMG,
                                String.format(Locale.ENGLISH, getString(R.string.file_name_body),
                                        type.substring(0, type.indexOf(" Code")), String.valueOf(System.currentTimeMillis())),
                                AppConstants.SUFFIX_IMG, Environment.DIRECTORY_PICTURES);

                        if (codeImageFile != null) {
                            try (FileOutputStream out = new FileOutputStream(codeImageFile)) {
                                result.getBitmap().compress(Bitmap.CompressFormat.PNG, 100, out);

                                code = new Code(result.getText(), result.getBarcodeFormat().name().toLowerCase().startsWith("qr")
                                        ? Code.QR_CODE : Code.BAR_CODE, codeImageFile.getPath(), result.getResult().getTimestamp());
                            } catch (IOException e) {
                                if (!TextUtils.isEmpty(e.getMessage())) {
                                    Log.e(getClass().getSimpleName(), Objects.requireNonNull(e.getMessage()));
                                }

                                code = new Code(result.getText(), result.getBarcodeFormat().name().toLowerCase().startsWith("qr")
                                        ? Code.QR_CODE : Code.BAR_CODE, result.getResult().getTimestamp());
                            }
                        } else {
                            code = new Code(result.getText(), result.getBarcodeFormat().name().toLowerCase().startsWith("qr") ?
                                    Code.QR_CODE : Code.BAR_CODE, result.getResult().getTimestamp());
                        }
                    } else {
                        code = new Code(result.getText(), result.getBarcodeFormat().name().toLowerCase().startsWith("qr") ?
                                Code.QR_CODE : Code.BAR_CODE, result.getResult().getTimestamp());
                    }

                    Intent intent = new Intent(_context, ScanResultActivity.class);
                    intent.putExtra(IntentKey.MODEL, code);
                    startActivity(intent);
                } else {
                    _barcodeView.resume();
                    doScan();
                    Toast.makeText(_context, getString(R.string.error_occured_while_scanning), Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void possibleResultPoints(List<ResultPoint> resultPoints) {}
        });
    }

    private void doPreRequisites() {
        _beepManager = new BeepManager(_activity);
        _beepManager.setVibrateEnabled(SharedPrefUtil.readBooleanDefaultTrue(PreferenceKey.VIBRATE));
        _beepManager.setBeepEnabled(SharedPrefUtil.readBooleanDefaultTrue(PreferenceKey.PLAY_SOUND));
        _barcodeView.setStatusText(AppConstants.EMPTY_STRING);
    }

    private void initializeViews(@NonNull View view) {
        _textViewFlash = view.findViewById(R.id.text_view_set_flash);
        _textViewScanGallery = view.findViewById(R.id.text_view_scan_gallery);
        _barcodeView = view.findViewById(R.id.barcode_view);
    }

    private void setListeners() {
        _textViewFlash.setOnClickListener(this);
        _textViewScanGallery.setOnClickListener(this);
    }

    @Override
    public void onResume() {
        super.onResume();
        doPreRequisites();
        _barcodeView.resume();
        doScan();
    }

    @Override
    public void onPause() {
        super.onPause();
        _barcodeView.pause();
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.text_view_set_flash:
                if (_context == null)
                    return;

                Drawable flashIcon = ContextCompat.getDrawable(_context, _isFlashOn ? R.drawable.ic_flash_off : R.drawable.ic_flash_on);
                _textViewFlash.setCompoundDrawablesWithIntrinsicBounds(null, flashIcon, null, null);

                if (_isFlashOn) {
                    _barcodeView.setTorchOff();
                } else {
                    _barcodeView.setTorchOn();
                }

                _isFlashOn = !_isFlashOn;
                break;

            case R.id.text_view_scan_gallery:
                ImagePicker.pickImage(this);
                break;

            default:
                break;
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == ImagePicker.REQUEST_CODE_PICK_IMAGE && _context != null) {
            ProgressDialogUtil.on().showProgressDialog(_context);
            Bitmap bitmap = ImagePicker.getPickedImageFromResult(_context, resultCode, data);
            Result result = processBitmapToGetResult(bitmap);

            if (result != null) {
                ImageInfo imageInfo = ImagePicker.getPickedImageInfo(_context, resultCode, data);

                if (imageInfo != null && imageInfo.getImageUri() != null) {
                    String imagePath = getPathFromUri(imageInfo.getImageUri());

                    if (!TextUtils.isEmpty(imagePath)) {
                        int typeIndex = result.getBarcodeFormat().name().toLowerCase().startsWith("qr") ? Code.QR_CODE : Code.BAR_CODE;

                        Code code = new Code(result.getText(), typeIndex, imagePath, result.getTimestamp());
                        Intent intent = new Intent(_context, PickedFromGalleryActivity.class);
                        intent.putExtra(IntentKey.MODEL, code);
                        startActivity(intent);
                    } else {
                        Toast.makeText(_context, getString(R.string.error_did_not_find_any_content),
                                Toast.LENGTH_SHORT).show();
                    }
                } else {
                    Toast.makeText(_context, getString(R.string.error_did_not_find_any_content),
                            Toast.LENGTH_SHORT).show();
                }
            }
        }
    }

    private Result processBitmapToGetResult(Bitmap bitmap) {
        if (bitmap != null) {
            int[] intArray = new int[bitmap.getWidth() * bitmap.getHeight()];

            bitmap.getPixels(intArray, 0, bitmap.getWidth(), 0, 0, bitmap.getWidth(), bitmap.getHeight());
            LuminanceSource source = new RGBLuminanceSource(bitmap.getWidth(), bitmap.getHeight(), intArray);
            BinaryBitmap binaryBitmap = new BinaryBitmap(new HybridBinarizer(source));

            Reader reader = new MultiFormatReader();

            try {
                Hashtable<DecodeHintType, Object> decodeHints = new Hashtable<>();
                decodeHints.put(DecodeHintType.TRY_HARDER, Boolean.TRUE);

                Result result = reader.decode(binaryBitmap, decodeHints);
                String codeResult = result.getText();

                if (!TextUtils.isEmpty(codeResult)) {
                    ProgressDialogUtil.on().hideProgressDialog();
                    return result;
                } else {
                    ProgressDialogUtil.on().hideProgressDialog();
                    Toast.makeText(_context, getString(R.string.error_did_not_find_any_content),
                            Toast.LENGTH_SHORT).show();
                    return null;
                }
            } catch (Exception e) {
                ProgressDialogUtil.on().hideProgressDialog();
                Toast.makeText(_context, getString(R.string.error_did_not_find_any_content),
                        Toast.LENGTH_SHORT).show();

                if (!TextUtils.isEmpty(e.getMessage())) {
                    Log.d(getClass().getSimpleName(), Objects.requireNonNull(e.getMessage()));
                }
                return null;
            }
        } else {
            ProgressDialogUtil.on().hideProgressDialog();
            Toast.makeText(_context, getString(R.string.error_could_not_load_the_image),
                    Toast.LENGTH_SHORT).show();
            return null;
        }
    }

    private String getPathFromUri(Uri uri) {
        if (_context == null) {
            return null;
        }

        String[] data = {MediaStore.Images.Media.DATA};
        CursorLoader loader = new CursorLoader(_context, uri, data, null, null, null);
        Cursor cursor = loader.loadInBackground();
        if (cursor == null) {
            return null;
        }

        int column_index = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
        cursor.moveToFirst();
        return cursor.getString(column_index);
    }
}
