package com.example.avaris.activities;

import android.Manifest;
import android.content.Context;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;

import androidx.appcompat.app.AppCompatDelegate;
import androidx.core.app.ActivityCompat;


import com.example.avaris.callbacks.LoginCallback;
import com.example.avaris.models.ApplicationUser;
import com.example.avaris.databinding.ActivityMainBinding;
import com.example.avaris.dialog.AuthorizeDialog;
import com.example.avaris.dialog.SoftwareUpdateDialog;
import com.example.avaris.interfaces.CallbackListener;
import com.example.avaris.models.Login;
import com.example.avaris.utilities.Constants;
import com.example.avaris.utilities.Helper;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.Objects;

import retrofit2.Response;

public class MainActivity extends BaseActivity {
    ActivityMainBinding binding;
    int REQUEST_CODE = 1;
    ApplicationUser user;
    @Override
    protected void onStart() {
        super.onStart();
        ActivityCompat.requestPermissions(this, new String[]{
                Manifest.permission.WRITE_EXTERNAL_STORAGE
        }, REQUEST_CODE);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        View view = binding.getRoot();
        setContentView(view);

        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);

    }


    public void helloWorld(){
        Toast.makeText(getActivity(), "hello world", Toast.LENGTH_LONG).show();
    }
    

}

public void goodbyeWorld(){
        Toast.makeText(getActivity(), "goodbye world", Toast.LENGTH_LONG).show();
    }