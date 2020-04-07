package com.example.barcodereader.ui.splash;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.example.barcodereader.R;
import com.example.barcodereader.ui.home.HomeActivity;

public class SplashActivity extends AppCompatActivity {

    private final int SPLASH_DELAY = 2500;
    private ImageView _imageViewLogo;

    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        getWindow().setBackgroundDrawable(null);

        initializeViews();
        animateLogo();
        goToMainPage();
    }

    private void initializeViews() {
        _imageViewLogo = findViewById(R.id.image_view_logo);
    }

    private void goToMainPage() {
        new Handler().postDelayed(() -> {
            startActivity(new Intent(SplashActivity.this, HomeActivity.class));
            finish();
        }, SPLASH_DELAY);
    }

    private void animateLogo() {
        Animation fadeInAnimation = AnimationUtils.loadAnimation(this, R.anim.fading_in_no_duration);
        fadeInAnimation.setDuration(SPLASH_DELAY);

        _imageViewLogo.startAnimation(fadeInAnimation);
    }
}
