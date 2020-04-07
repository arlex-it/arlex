package com.example.barcodereader.ui.home;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.databinding.DataBindingUtil;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentTransaction;

import com.example.barcodereader.R;
import com.example.barcodereader.databinding.ActivityMainBinding;
import com.example.barcodereader.helpers.constant.PreferenceKey;
import com.example.barcodereader.helpers.util.PermissionUtil;
import com.example.barcodereader.helpers.util.SharedPrefUtil;
import com.example.barcodereader.ui.generate.GenerateFragment;
import com.example.barcodereader.ui.history.HistoryFragment;
import com.example.barcodereader.ui.scan.ScanFragment;
import com.example.barcodereader.ui.settings.SettingsActivity;
import com.github.pwittchen.reactivenetwork.library.rx2.ReactiveNetwork;
import com.google.android.gms.ads.AdListener;
import com.google.android.gms.ads.AdRequest;
import com.google.zxing.integration.android.IntentIntegrator;

import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.CompositeDisposable;
import io.reactivex.schedulers.Schedulers;

public class HomeActivity extends AppCompatActivity implements View.OnClickListener {

    private ActivityMainBinding _binding;
    //private ActivityHomeBinding _binding;
    private Menu _toolbarMenu;

    public Menu getToolbarMenu() {
        return _toolbarMenu;
    }

    public void setToolbarMenu(Menu toolbarMenu) {
        _toolbarMenu = toolbarMenu;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        _binding = DataBindingUtil.setContentView(this, R.layout.activity_main);

        getWindow().setBackgroundDrawable(null);

        setListeners();
        initializeToolbar();
        initializeBottomBar();
        checkInternetConnection();
        playAd();
    }

    private void checkInternetConnection() {
        CompositeDisposable disposable = new CompositeDisposable();
        disposable.add(ReactiveNetwork.observeNetworkConnectivity(this).subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread()).subscribe(connectivity -> {
                    if (connectivity.state() == NetworkInfo.State.CONNECTED) {
                        _binding.adView.setVisibility(View.VISIBLE);
                    } else {
                        _binding.adView.setVisibility(View.GONE);
                    }
                }, throwable -> {
                    Toast.makeText(this, getString(R.string.something_wrong), Toast.LENGTH_SHORT).show();
                }));
    }

    private void playAd() {
        AdRequest adRequest = new AdRequest.Builder().build();

        _binding.adView.loadAd(adRequest);
        _binding.adView.setAdListener(new AdListener() {
            @Override
            public void onAdLoaded() {
            }

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

    private void initializeToolbar() {
        //setSupportActionBar(_binding.toolbar);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.home_toolbar_menu, menu);
        setToolbarMenu(menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.action_settings:
                startActivity(new Intent(this, SettingsActivity.class));
                return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void setListeners() {
        _binding.textViewGenerate.setOnClickListener(this);
        _binding.textViewScan.setOnClickListener(this);
        _binding.textViewHistory.setOnClickListener(this);

        _binding.imageViewGenerate.setOnClickListener(this);
        _binding.imageViewScan.setOnClickListener(this);
        _binding.imageViewHistory.setOnClickListener(this);

        _binding.constraintLayoutGenerateContainer.setOnClickListener(this);
        _binding.constraintLayoutScanContainer.setOnClickListener(this);
        _binding.constraintLayoutHistoryContainer.setOnClickListener(this);
    }

    private void initializeBottomBar() {
        clickOnScan();
    }

    private void clickOnGenerate() {
        _binding.textViewGenerate.setTextColor(ContextCompat.getColor(this, R.color.bottom_bar_selected));
        _binding.textViewScan.setTextColor(ContextCompat.getColor(this, R.color.bottom_bar_normal));
        _binding.textViewHistory.setTextColor(ContextCompat.getColor(this, R.color.bottom_bar_normal));

        _binding.imageViewGenerate.setVisibility(View.INVISIBLE);
        _binding.imageViewGenerateActive.setVisibility(View.VISIBLE);

        _binding.imageViewScan.setVisibility(View.VISIBLE);
        _binding.imageViewScanActive.setVisibility(View.INVISIBLE);

        _binding.imageViewHistory.setVisibility(View.VISIBLE);
        _binding.imageViewHistoryActive.setVisibility(View.INVISIBLE);

        setToolbarTitle(getString(R.string.toolbar_title_generate));
        showFragment(GenerateFragment.newInstance());
    }

    private void clickOnScan() {
        if (PermissionUtil.on().requestPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.CAMERA)) {
            _binding.textViewGenerate.setTextColor(ContextCompat.getColor(this, R.color.bottom_bar_normal));
            _binding.textViewScan.setTextColor(ContextCompat.getColor(this, R.color.bottom_bar_selected));
            _binding.textViewHistory.setTextColor(ContextCompat.getColor(this, R.color.bottom_bar_normal));

            _binding.imageViewGenerate.setVisibility(View.VISIBLE);
            _binding.imageViewGenerateActive.setVisibility(View.INVISIBLE);

            _binding.imageViewScan.setVisibility(View.INVISIBLE);
            _binding.imageViewScanActive.setVisibility(View.VISIBLE);

            _binding.imageViewHistory.setVisibility(View.VISIBLE);
            _binding.imageViewHistoryActive.setVisibility(View.INVISIBLE);

            setToolbarTitle(getString(R.string.toolbar_title_scan));
            showFragment(ScanFragment.newInstance());

            /*IntentIntegrator integrator = new IntentIntegrator(this);
            integrator.setBeepEnabled(SharedPrefUtil.readBooleanDefaultTrue(PreferenceKey.PLAY_SOUND));
            integrator.setOrientationLocked(false);
            integrator.setPrompt("Scan a barcode");
            integrator.initiateScan();
            integrator.setDesiredBarcodeFormats(IntentIntegrator.ONE_D_CODE_TYPES);*/
        }
    }

    private void clickOnHistory() {
        _binding.textViewGenerate.setTextColor(ContextCompat.getColor(this, R.color.bottom_bar_normal));
        _binding.textViewScan.setTextColor(ContextCompat.getColor(this, R.color.bottom_bar_normal));
        _binding.textViewHistory.setTextColor(ContextCompat.getColor(this, R.color.bottom_bar_selected));

        _binding.imageViewGenerate.setVisibility(View.VISIBLE);
        _binding.imageViewGenerateActive.setVisibility(View.INVISIBLE);

        _binding.imageViewScan.setVisibility(View.VISIBLE);
        _binding.imageViewScanActive.setVisibility(View.INVISIBLE);

        _binding.imageViewHistory.setVisibility(View.INVISIBLE);
        _binding.imageViewHistoryActive.setVisibility(View.VISIBLE);

        setToolbarTitle(getString(R.string.toolbar_title_history));
        showFragment(HistoryFragment.newInstance());
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.image_view_generate:
            case R.id.text_view_generate:
            case R.id.constraint_layout_generate_container:
                clickOnGenerate();
                break;

            case R.id.image_view_scan:
            case R.id.text_view_scan:
            case R.id.constraint_layout_scan_container:
                clickOnScan();
                break;

            case R.id.image_view_history:
            case R.id.text_view_history:
            case R.id.constraint_layout_history_container:
                clickOnHistory();
                break;
        }
    }

    private void setToolbarTitle(String title) {
        if (getSupportActionBar() != null) {
            getSupportActionBar().setTitle(title);
        }
    }

    private void showFragment(Fragment fragment) {
        FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
        transaction.replace(R.id.coordinator_layout_fragment_container, fragment, fragment.getClass().getSimpleName());
        transaction.commit();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == PermissionUtil.REQUEST_CODE_PERMISSION_DEFAULT) {
            boolean isAllowed = true;

            for (int i = 0; i < permissions.length; i++) {
                if (grantResults[i] != PackageManager.PERMISSION_GRANTED) {
                    isAllowed = false;
                }
            }

            if (isAllowed) {
                clickOnScan();
            }
        }
    }

    /*public void hideAdMob() {
        if (_binding.adView.isShown())
            _binding.adView.setVisibility(View.GONE);
    }

    public void showAdMob() {
        if (!_binding.adView.isShown())
            _binding.adView.setVisibility(View.VISIBLE);
    }*/
}
