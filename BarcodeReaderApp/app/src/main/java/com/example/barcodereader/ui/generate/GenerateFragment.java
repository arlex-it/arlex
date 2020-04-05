package com.example.barcodereader.ui.generate;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.core.content.ContextCompat;
import androidx.databinding.DataBindingUtil;

import com.example.barcodereader.R;
import com.example.barcodereader.databinding.FragmentGenerateBinding;
import com.example.barcodereader.helpers.constant.IntentKey;
import com.example.barcodereader.helpers.model.Code;
import com.example.barcodereader.ui.generatedcode.GeneratedCodeActivity;
import com.google.android.gms.ads.AdListener;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.InterstitialAd;

import org.jetbrains.annotations.NotNull;

public class GenerateFragment extends androidx.fragment.app.Fragment implements View.OnClickListener {

    private FragmentGenerateBinding _binding;
    private Context _context;
    private InterstitialAd _interstitialAd;

    public GenerateFragment() {}

    public static GenerateFragment newInstance() {
        return new GenerateFragment();
    }

    @Override
    public void onAttach(@NotNull Context context) {
        super.onAttach(context);
        _context = context;
    }

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        _binding = DataBindingUtil.inflate(inflater, R.layout.fragment_generate, container, false);
        initializeAd();
        setListeners();
        initializeCodeTypesSpinner();
        return _binding.getRoot();
    }

    @Override
    public void onResume() {
        super.onResume();
        _interstitialAd.loadAd(new AdRequest.Builder().build());
    }

    private void initializeAd() {
        if (_context == null) {
            return;
        }
        _interstitialAd = new InterstitialAd(_context);
        _interstitialAd.setAdUnitId(getString(R.string.admob_test_interstitial_ad_unit_id));
    }

    private void setListeners() {
        _binding.spinnerTypes.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                ((TextView)parent.getSelectedView()).setTextColor(ContextCompat.getColor(_context,
                        position == 0 ? R.color.text_hint : R.color.text_regular));
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {}
        });

        _binding.textViewGenerate.setOnClickListener(this);

        _interstitialAd.setAdListener(new AdListener() {
            @Override
            public void onAdLoaded() {}

            @Override
            public void onAdOpened() {}

            @Override
            public void onAdLeftApplication() {}

            @Override
            public void onAdClosed() {
                generateCode();
            }
        });
    }

    private void initializeCodeTypesSpinner() {
        ArrayAdapter arrayAdapter = ArrayAdapter.createFromResource(_context, R.array.code_types,
                android.R.layout.simple_spinner_item);
        arrayAdapter.setDropDownViewResource(R.layout.item_spinner);
        _binding.spinnerTypes.setAdapter(arrayAdapter);
    }

    @Override
    public void onClick(View view) {
        if (_context == null) {
            return;
        }

        if (view.getId() == R.id.text_view_generate) {
            if (_interstitialAd.isLoaded()) {
                _interstitialAd.show();
            } else {
                generateCode();
            }
        }
    }

    private void generateCode() {
        Intent intent = new Intent(_context, GeneratedCodeActivity.class);
        if (_binding.editTextContent.getText() != null) {
            String content = _binding.editTextContent.getText().toString().trim();
            int type = _binding.spinnerTypes.getSelectedItemPosition();

            if (!TextUtils.isEmpty(content) && type != 0) {
                boolean isValid = true;
                if (type == Code.BAR_CODE) {
                    if (content.length() > 80) {
                        Toast.makeText(_context, getString(R.string.error_qrcode_content_limit),
                                Toast.LENGTH_SHORT).show();
                        isValid = false;
                    }
                } else {
                    isValid = false;
                }

                if (isValid) {
                    Code code = new Code(content, type);
                    intent.putExtra(IntentKey.MODEL, code);
                    startActivity(intent);
                }
            } else {
                Toast.makeText(_context, getString(R.string.error_provide_proper_content_and_type),
                        Toast.LENGTH_SHORT).show();
            }
        }
    }
}
