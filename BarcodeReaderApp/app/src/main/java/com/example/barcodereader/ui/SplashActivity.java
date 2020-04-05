package com.example.barcodereader.ui;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;

import com.example.barcodereader.MainActivity;
import com.example.barcodereader.R;

public class SplashActivity extends AppCompatActivity {

    // Loading screen of 2 seconds
    private final int SPLASH_DELAY = 2000;
    private ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        getWindow().setBackgroundDrawable(null);

        setView();
        animateView();
        switchToMain();
    }

    private void setView() {
        //imageView = findViewById(R.id.imageView);
    }

    private void animateView() {
        Animation fadingInAnim = AnimationUtils.loadAnimation(this, R.anim.fading_in_no_duration);
        fadingInAnim.setDuration(SPLASH_DELAY);

        imageView.startAnimation(fadingInAnim);
    }

    private void switchToMain() {
        new Handler().postDelayed(()-> {
            startActivity(new Intent(SplashActivity.this, MainActivity.class));
            finish();
        }, SPLASH_DELAY);
    }
}