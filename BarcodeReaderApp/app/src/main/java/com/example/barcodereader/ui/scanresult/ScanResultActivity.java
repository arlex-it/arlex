package com.example.barcodereader.ui.scanresult;

import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.net.NetworkInfo;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.URLUtil;
import android.widget.Toast;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;
import androidx.databinding.DataBindingUtil;

import com.bumptech.glide.Glide;
import com.example.barcodereader.R;
import com.example.barcodereader.databinding.ActivityScanResultBinding;
import com.example.barcodereader.helpers.constant.IntentKey;
import com.example.barcodereader.helpers.constant.PreferenceKey;
import com.example.barcodereader.helpers.model.Code;
import com.example.barcodereader.helpers.util.SharedPrefUtil;
import com.example.barcodereader.helpers.util.TimeUtil;
import com.example.barcodereader.helpers.util.database.DatabaseUtil;
import com.example.barcodereader.ui.settings.SettingsActivity;
import com.github.pwittchen.reactivenetwork.library.rx2.ReactiveNetwork;
import com.google.android.gms.ads.AdListener;
import com.google.android.gms.ads.AdRequest;

import java.io.File;
import java.util.Locale;

import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.CompositeDisposable;
import io.reactivex.observers.DisposableCompletableObserver;
import io.reactivex.schedulers.Schedulers;

public class ScanResultActivity extends AppCompatActivity implements View.OnClickListener {

    private CompositeDisposable _compositeDisposable;
    private ActivityScanResultBinding _binding;
    private Menu _toolbarMenu;
    private Code _currentCode;
    private boolean _isHistory, _isPickedFromGallery;

    public CompositeDisposable getCompositeDisposable() {
        return _compositeDisposable;
    }

    public void setCompositeDisposable(CompositeDisposable compositeDisposable) {
        _compositeDisposable = compositeDisposable;
    }

    public Code getCurrentCode() {
        return _currentCode;
    }

    public void setCurrentCode(Code currentCode) {
        _currentCode = currentCode;
    }

    public Menu getToolbarMenu() {
        return _toolbarMenu;
    }

    public void setToolbarMenu(Menu toolbarMenu) {
        _toolbarMenu = toolbarMenu;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        _binding = DataBindingUtil.setContentView(this, R.layout.activity_scan_result);
        setCompositeDisposable(new CompositeDisposable());
        playAd();
        getWindow().setBackgroundDrawable(null);
        initializeToolbar();
        loadQRCode();
        setListeners();
        checkInternetConnection();
    }

    private void playAd() {
        AdRequest adRequest = new AdRequest.Builder().build();
        _binding.adView.loadAd(adRequest);
        _binding.adView.setAdListener(new AdListener() {
            @Override
            public void onAdLoaded() {}

            @Override
            public void onAdFailedToLoad(int errorCode) {
                _binding.adView.setVisibility(View.GONE);
            }

            @Override
            public void onAdOpened() {}

            @Override
            public void onAdLeftApplication() {}

            @Override
            public void onAdClosed() {}
        });
    }

    private void checkInternetConnection() {
        CompositeDisposable disposable = new CompositeDisposable();
        disposable.add(ReactiveNetwork.observeNetworkConnectivity(this)
                .subscribeOn(Schedulers.io()).observeOn(AndroidSchedulers.mainThread()).subscribe(connectivity -> {
                    if (connectivity.state() == NetworkInfo.State.CONNECTED) {
                        _binding.adView.setVisibility(View.VISIBLE);
                    } else {
                        _binding.adView.setVisibility(View.GONE);
                    }
                }, throwable -> {
                    Toast.makeText(this, getString(R.string.something_wrong), Toast.LENGTH_SHORT).show();
                }));
    }

    private void setListeners() {
        _binding.textViewOpenInBrowser.setOnClickListener(this);
        _binding.imageViewShare.setOnClickListener(this);
    }

    private void loadQRCode() {
        Intent intent = getIntent();

        if (intent != null) {
            Bundle bundle = intent.getExtras();

            if (bundle != null && bundle.containsKey(IntentKey.MODEL)) {
                setCurrentCode(bundle.getParcelable(IntentKey.MODEL));
            }
            if (bundle != null && bundle.containsKey(IntentKey.IS_HISTORY)) {
                _isHistory = bundle.getBoolean(IntentKey.IS_HISTORY);
            }
            if (bundle != null && bundle.containsKey(IntentKey.IS_PICKED_FROM_GALLERY)) {
                _isPickedFromGallery = bundle.getBoolean(IntentKey.IS_PICKED_FROM_GALLERY);
            }
        }

        if (getCurrentCode() != null) {
            _binding.textViewContent.setText(String.format(Locale.ENGLISH, getString(R.string.content),
                    getCurrentCode().getContent()));

            _binding.textViewType.setText(String.format(Locale.ENGLISH, getString(R.string.code_type),
                    getResources().getStringArray(R.array.code_types)[getCurrentCode().getType()]));

            _binding.textViewTime.setText(String.format(Locale.ENGLISH, getString(R.string.created_time),
                    TimeUtil.getFormattedDateString(getCurrentCode().getTimestamp())));

            _binding.textViewOpenInBrowser.setEnabled(URLUtil.isValidUrl(getCurrentCode().getContent()));

            if (!TextUtils.isEmpty(getCurrentCode().getImagePath())) {
                Glide.with(this).asBitmap().load(getCurrentCode().getImagePath()).into(_binding.imageViewScannedCode);
            }

            if (SharedPrefUtil.readBooleanDefaultTrue(PreferenceKey.COPY_TO_CLIPBOARD) && !_isHistory) {
                ClipboardManager clipboardManager = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);

                if (clipboardManager != null) {
                    ClipData clipData = ClipData.newPlainText(getString(R.string.scanned_qr_code_content),
                            getCurrentCode().getContent());
                    clipboardManager.setPrimaryClip(clipData);

                    Toast.makeText(this, getString(R.string.copied_to_clipboard), Toast.LENGTH_SHORT).show();
                }
            }

            if (SharedPrefUtil.readBooleanDefaultTrue(PreferenceKey.SAVE_HISTORY) && !_isHistory) {
                getCompositeDisposable().add(DatabaseUtil.on().insertCode(getCurrentCode()).
                        observeOn(AndroidSchedulers.mainThread()).subscribeOn(Schedulers.io()).
                        subscribeWith(new DisposableCompletableObserver() {
                            @Override
                            public void onComplete() {}

                            @Override
                            public void onError(Throwable e) {}
                        }));
            }
        }
    }

    private void initializeToolbar() {
        setSupportActionBar(_binding.toolbar);

        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.setDisplayShowHomeEnabled(true);
            actionBar.setDisplayHomeAsUpEnabled(true);
        }
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

    @Override public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.home_toolbar_menu, menu);
        setToolbarMenu(menu);
        return true;
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.text_view_open_in_browser:
                if (getCurrentCode() != null && URLUtil.isValidUrl(getCurrentCode().getContent())) {
                    Intent browserIntent = new Intent(Intent.ACTION_VIEW);
                    browserIntent.setData(Uri.parse(getCurrentCode().getContent()));
                    startActivity(browserIntent);
                }
                break;

            case R.id.image_view_share:
                if (getCurrentCode() != null) {
                    shareCode(new File(getCurrentCode().getImagePath()));
                }
                break;

            default:
                break;
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        getCompositeDisposable().dispose();

        if (getCurrentCode() != null && !SharedPrefUtil.readBooleanDefaultTrue(PreferenceKey.SAVE_HISTORY) &&
                !_isHistory && !_isPickedFromGallery) {
            new File(getCurrentCode().getImagePath()).delete();
        }
    }

    private void shareCode(File codeImageFile) {
        Intent shareIntent = new Intent(Intent.ACTION_SEND);
        shareIntent.setType("image/*");

        if (Build.VERSION.SDK_INT > Build.VERSION_CODES.M) {
            shareIntent.putExtra(Intent.EXTRA_STREAM, FileProvider.getUriForFile(this,
                    getString(R.string.file_provider_authority), codeImageFile));
            shareIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        } else {
            shareIntent.putExtra(Intent.EXTRA_STREAM, Uri.fromFile(codeImageFile));
        }

        startActivity(Intent.createChooser(shareIntent, getString(R.string.share_code_using)));
    }

}
