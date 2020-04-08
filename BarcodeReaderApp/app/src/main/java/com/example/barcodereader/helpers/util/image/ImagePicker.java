package com.example.barcodereader.helpers.util.image;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ResolveInfo;
import android.content.res.AssetFileDescriptor;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.net.Uri;
import android.os.Parcelable;
import android.provider.MediaStore;
import android.util.Log;

import androidx.fragment.app.Fragment;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;

public class ImagePicker {

    public final static int REQUEST_CODE_PICK_IMAGE = 15913;
    private final static int DEF_MIN_WIDTH = 400;
    private final static String TITLE = "Pick Image";

    private ImagePicker() {}

    // pick img from gallery & photos from camera
    public synchronized static void pickImage(Activity activity) {
        if (activity != null) {
            Intent imagePickingIntent = getImagePickingIntent(activity);

            if (imagePickingIntent != null)
                activity.startActivityForResult(imagePickingIntent, REQUEST_CODE_PICK_IMAGE);
        }
    }

    // same for fragment
    public synchronized static void pickImage(Fragment fragment) {
        if (fragment != null && fragment.getContext() != null) {
            Intent imagePickingIntent = getImagePickingIntent(fragment.getContext());

            if (imagePickingIntent != null)
                fragment.startActivityForResult(imagePickingIntent, REQUEST_CODE_PICK_IMAGE);
        }
    }

    // choose an image in the phone's gallery
    public static Intent getImagePickingIntent(Context context) {
        if (context == null)
            return null;

        Intent choose = null;
        List<Intent> intents = new ArrayList<>();
        Intent photoPicked = new Intent();

        photoPicked.setType("image/*");
        photoPicked.setAction(Intent.ACTION_GET_CONTENT);
        intents = addIntentsToList(context, intents, photoPicked);

        if (intents.size() > 0) {
            choose = Intent.createChooser(intents.remove(intents.size() - 1), TITLE);
            choose.putExtra(Intent.EXTRA_INITIAL_INTENTS, intents.toArray(new Parcelable[]{}));
        }
        return choose;
    }

    // info of the image
    public static ImageInfo getPickedImageInfo(Context context, int res, Intent image) {
        if (context == null || res != Activity.RESULT_OK)
            return null;

        return new ImageInfo(image.getData(), false);
    }

    // get bitmap's image
    public static Bitmap getPickedImageFromResult(Context context, int res, Intent image) {
        if (context == null || res != Activity.RESULT_OK)
            return null;

        Log.d("Result code", String.valueOf(res));

        ImageInfo pickedImageInfo = getPickedImageInfo(context, res, image);
        if (pickedImageInfo.getImageUri() == null ||
                pickedImageInfo.getImageUri().getPath() == null)
            return null;

        Log.d("Selected image", pickedImageInfo.getImageUri().getPath());

        Bitmap bitmap = getImageResized(context, pickedImageInfo.getImageUri());
        int rotation = getRotation(context, pickedImageInfo.getImageUri());

        bitmap = rotate(bitmap, rotation);
        return bitmap;
    }

    private static List<Intent> addIntentsToList(Context context, List<Intent> intents,
                                                 Intent intent) {
        if (context == null || intent == null)
            return intents;

        List<ResolveInfo> resolveInfos = context.getPackageManager()
                                                .queryIntentActivities(intent, 0);

        for (ResolveInfo resolveInfo : resolveInfos) {
            String packageName = resolveInfo.activityInfo.packageName;

            Intent target = new Intent(intent);
            target.setPackage(packageName);

            intents.add(target);
            Log.d("Intent", intent.getAction() + " package: " + packageName);
        }
        return intents;
    }

    private static Bitmap getImageResized(Context context, Uri imageUri) {
        if (context == null || imageUri == null)
            return null;

        Bitmap bitmap;
        int[] sizes = new int[]{5, 3, 2, 1};
        int i = 0;

        do {
            bitmap = decodeBitmap(context, imageUri, sizes[i]);
            Log.d("Resizer", "new bitmap width = " + bitmap.getWidth());
            ++i;
        } while (bitmap.getWidth() < DEF_MIN_WIDTH && i < sizes.length);

        return bitmap;
    }

    private static Bitmap decodeBitmap(Context context, Uri imageUri, int size) {
        if (context == null || imageUri == null) {
            return null;
        }

        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inSampleSize = size;

        AssetFileDescriptor fileDescriptor = null;
        try {
            fileDescriptor = context.getContentResolver()
                                    .openAssetFileDescriptor(imageUri, "r");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        Bitmap actuallyUsableBitmap = null;

        if (fileDescriptor != null) {
            actuallyUsableBitmap = BitmapFactory.decodeFileDescriptor(
                    fileDescriptor.getFileDescriptor(), null, options
            );

            Log.d("Decode bitmap", options.inSampleSize + " sample method bitmap " +
                    actuallyUsableBitmap.getWidth() + " " + actuallyUsableBitmap.getHeight());
        }
        return actuallyUsableBitmap;
    }

    private static int getRotation(Context context, Uri imageUri) {
        int rotation = getRotationFromGallery(context, imageUri);

        Log.d("Image rotation", String.valueOf(rotation));

        return rotation;
    }

    private static int getRotationFromGallery(Context context, Uri imageUri) {
        if (context == null || imageUri == null)
            return 0;

        int result = 0;
        String[] columns = {MediaStore.Images.Media.ORIENTATION};
        try (Cursor cursor = context.getContentResolver().query(
                imageUri, columns, null, null, null
        )) {

            if (cursor != null && cursor.moveToFirst())
                result = cursor.getInt(cursor.getColumnIndex(columns[0]));

        } catch (Exception ignored) {}

        return result;
    }

    private static Bitmap rotate(Bitmap bitmap, int rotation) {
        if (rotation != 0) {
            Matrix matrix = new Matrix();
            matrix.postRotate(rotation);
            return Bitmap.createBitmap(bitmap, 0, 0, bitmap.getWidth(), bitmap.getHeight(), matrix, true);
        }
        return bitmap;
    }

}
