package com.example.barcodereader.ui.settings;

import android.content.Intent;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import android.widget.CompoundButton;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import com.example.barcodereader.R;
import com.example.barcodereader.databinding.ActivitySettingsBinding;
import com.example.barcodereader.helpers.constant.PreferenceKey;
import com.example.barcodereader.helpers.util.SharedPrefUtil;
import com.example.barcodereader.ui.about_us.AboutUsActivity;
import com.example.barcodereader.ui.privacy_policy.PrivacyPolicyActivity;
import com.google.android.gms.common.internal.safeparcel.SafeParcelable;

public class SettingsActivity extends AppCompatActivity implements CompoundButton.OnCheckedChangeListener, View.OnClickListener {

    private ActivitySettingsBinding _binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        _binding = DataBindingUtil.setContentView(this, R.layout.activity_settings);

        initializeToolbar();
        loadSettings();
        setListeners();
    }

    private void loadSettings() {
        _binding.switchCompatPlaySound.setChecked(SharedPrefUtil.readBooleanDefaultTrue(PreferenceKey.PLAY_SOUND));
        _binding.switchCompatVibrate.setChecked(SharedPrefUtil.readBooleanDefaultTrue(PreferenceKey.VIBRATE));
        _binding.switchCompatSaveHistory.setChecked(SharedPrefUtil.readBooleanDefaultTrue(PreferenceKey.SAVE_HISTORY));
        _binding.switchCompatCopyToClipboard.setChecked(SharedPrefUtil.readBooleanDefaultTrue(PreferenceKey.COPY_TO_CLIPBOARD));
    }

    private void setListeners() {
        _binding.switchCompatPlaySound.setOnCheckedChangeListener(this);
        _binding.switchCompatVibrate.setOnCheckedChangeListener(this);
        _binding.switchCompatSaveHistory.setOnCheckedChangeListener(this);
        _binding.switchCompatCopyToClipboard.setOnCheckedChangeListener(this);
    }

    private void initializeToolbar() {
        setSupportActionBar(_binding.toolbar);

        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.setDisplayHomeAsUpEnabled(true);
            actionBar.setDisplayShowHomeEnabled(true);
        }
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                onBackPressed();
                break;

            default:
                break;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
        switch (buttonView.getId()) {
            case R.id.switch_compat_play_sound:
                SharedPrefUtil.write(PreferenceKey.PLAY_SOUND, isChecked);
                break;

            case R.id.switch_compat_vibrate:
                SharedPrefUtil.write(PreferenceKey.VIBRATE, isChecked);
                break;

            case R.id.switch_compat_save_history:
                SharedPrefUtil.write(PreferenceKey.SAVE_HISTORY, isChecked);
                break;

            case R.id.switch_compat_copy_to_clipboard:
                SharedPrefUtil.write(PreferenceKey.COPY_TO_CLIPBOARD, isChecked);
                break;

            default:
                break;
        }
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.text_view_play_sound:
                _binding.switchCompatPlaySound.setChecked(!_binding.switchCompatPlaySound.isChecked());
                break;

            case R.id.text_view_vibrate:
                _binding.switchCompatVibrate.setChecked(!_binding.switchCompatVibrate.isChecked());
                break;

            case R.id.text_view_save_history:
                _binding.switchCompatSaveHistory.setChecked(!_binding.switchCompatSaveHistory.isChecked());
                break;

            case R.id.text_view_copy_to_clipboard:
                _binding.switchCompatCopyToClipboard.setChecked(!_binding.switchCompatCopyToClipboard.isChecked());
                break;

            default:
                break;
        }
    }

    public void startAboutUsActivity(View view) {
        startActivity(new Intent(this, AboutUsActivity.class));
    }

    public void startPrivacyPolicyActivity(View view) {
        startActivity(new Intent(this, PrivacyPolicyActivity.class));
    }
}
