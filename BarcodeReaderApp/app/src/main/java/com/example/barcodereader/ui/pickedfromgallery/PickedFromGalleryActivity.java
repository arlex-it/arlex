package com.example.barcodereader.ui.pickedfromgallery;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import com.bumptech.glide.Glide;
import com.example.barcodereader.R;
import com.example.barcodereader.databinding.ActivityPickedFromGalleryBinding;
import com.example.barcodereader.helpers.constant.IntentKey;
import com.example.barcodereader.helpers.model.Code;
import com.example.barcodereader.ui.scanresult.ScanResultActivity;
import com.example.barcodereader.ui.settings.SettingsActivity;

public class PickedFromGalleryActivity extends AppCompatActivity implements View.OnClickListener {

    private ActivityPickedFromGalleryBinding _binding;
    private Code _currentCode;
    private Menu _toolbarMenu;

    public Menu getToolbarMenu() {
        return _toolbarMenu;
    }

    public void setToolbarMenu(Menu toolbarMenu) {
        _toolbarMenu = toolbarMenu;
    }

    public Code getCurrentCode() {
        return _currentCode;
    }

    public void setCurrentCode(Code currentCode) {
        _currentCode = currentCode;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        _binding = DataBindingUtil.setContentView(this, R.layout.activity_picked_from_gallery);

        initializeToolbar();
        loadQRCode();
        setListeners();
    }

    private void initializeToolbar() {
        setSupportActionBar(_binding.toolbar);

        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.setDisplayHomeAsUpEnabled(true);
            actionBar.setDisplayShowHomeEnabled(true);
        }
    }

    private void loadQRCode() {
        Intent intent = getIntent();

        if (intent != null) {
            Bundle bundle = intent.getExtras();
            if (bundle != null && bundle.containsKey(IntentKey.MODEL)) {
                setCurrentCode(bundle.getParcelable(IntentKey.MODEL));
            }
        }

        if (getCurrentCode() != null) {
            if (!TextUtils.isEmpty(getCurrentCode().getImagePath())) {
                Glide.with(this)
                        .asBitmap()
                        .load(getCurrentCode().getImagePath())
                        .into(_binding.imageViewScannedCode);
            }
        }
    }

    private void setListeners() {
        _binding.textViewGetValue.setOnClickListener(this);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                onBackPressed();
                break;

            case R.id.action_settings:
                startActivity(new Intent(this, SettingsActivity.class));
                return true;

            default:
                break;
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.text_view_get_value:
                if (getCurrentCode() != null) {
                    Intent intent = new Intent(this, ScanResultActivity.class);
                    intent.putExtra(IntentKey.MODEL, getCurrentCode());
                    intent.putExtra(IntentKey.IS_PICKED_FROM_GALLERY, true);
                    startActivity(intent);
                }
                break;
            default:
                break;
        }
    }
}
