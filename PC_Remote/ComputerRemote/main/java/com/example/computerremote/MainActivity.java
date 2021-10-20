package com.example.computerremote;

import android.graphics.Color;
import android.hardware.ConsumerIrManager;
import android.media.Image;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.SeekBar;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    // ====================================================
    // Functions used by views:

    private void btnEffect(final ImageButton btn) {
        final ImageButton powerOnBtn = findViewById(R.id.powerOnBtn);

        if(btn != powerOnBtn) {  // make the button white for 200ms
            btn.setColorFilter(Color.WHITE);
        } else {  // change power on colours to brighter red
            btn.setColorFilter(Color.parseColor("#ff0000"));
        }

        /* play button clicked sound
        final int[] sounds = {R.raw.do_19, R.raw.re_19, R.raw.mi_19, R.raw.fa_19, R.raw.sol_19,
                R.raw.la_19, R.raw.si_19, R.raw.do_upper_19, R.raw.do_upper_plus1_19, R.raw.do_upper_plus2_19};

        int randomIdx = new Random().nextInt(sounds.length);

        final MediaPlayer mp = MediaPlayer.create(this, sounds[randomIdx]);
        mp.start();

        mp.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
            public void onCompletion(MediaPlayer mp) {
                mp.release();
            }
        });
        */

        // turn colour back to original after 200 ms delay
        new android.os.Handler().postDelayed(
                new Runnable() {
                    public void run() {
                        if(btn != powerOnBtn) {
                            btn.setColorFilter(Color.parseColor("#b0afaf"));  // set it back to grey
                        } else {
                            btn.setColorFilter(Color.parseColor("#800006"));  // if it is power on button set to red colour
                        }
                    }
                },
                200);
    }


    // ====================================================
    // General functions:

    private void transmitSignal(final int[] signalPattern) {
        final int frequency = 38000;

        //for (int i = 0; i < 3; ++i) {  // repeat it 3 times to make sure the signal was correctly received
            Log.d(TAG, "transmitSignal: trying to transmit IR signal");
            try {
                ConsumerIrManager consumerIrManager = (ConsumerIrManager) getSystemService(CONSUMER_IR_SERVICE);
                if (!consumerIrManager.hasIrEmitter()) {
                    Log.d(TAG, "transmitSignal: Device does not support IR functionality");
                    return;
                }
                // int[] pattern = new int[] {250000, 250000, 250000, 250000, 250000, 250000, 250000, 250000};
                //int[] pattern = new int[] {4495,4368,546,1638,546,1638,546,1638,546,546,546,546,546,546,546,546,546,546,546,1638,546,1638,546,1638,546,546,546,546,546,546,546,546,546,546,546,546,546,1638,546,546,546,546,546,546,546,546,546,546,546,546,546,1664,546,546,546,1638,546,1638,546,1638,546,1638,546,1638,546,1638,546,46644,4394,4368,546,546,546,96044};
                // above line outputs decoded signal: 3772793023
                consumerIrManager.transmit(frequency, signalPattern);
                Log.d(TAG, "transmitSignal: transmitting the IR signal successful");
            } catch (SecurityException e) {
                Log.d(TAG, "transmitSignal: Security Exception raised. Missing PERMISSION ?" + e.getMessage());
                e.printStackTrace();
            }
        //}
    }


    // ====================================================
    // Global variables:

    // IR hex codes for all commands:
    private final int[][] buttonsSignalPatterns = {
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 624, 624, 624, 624, 1248, 624},  // 4081
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 624, 624, 1248, 624, 624, 624},  // 4082...
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 624, 624, 1248, 624, 1248, 624},
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 1248, 624, 624, 624, 624, 624},
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 1248, 624, 624, 624, 1248, 624}  // 4085
    };

    private final int[][] playerVolumeSignalPatterns = {
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 1248, 624, 1248, 624, 624, 624},  // 4086
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 1248, 624, 1248, 624, 1248, 624},  // 4087...
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 624, 624, 624, 624},
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 624, 624, 1248, 624},
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 1248, 624, 624, 624},
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 1248, 624, 1248, 624},
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 624, 624},
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624, 1248, 624},
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624},
        {1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624}  // 4096
    };

    private final int[][] pcVolumeSignalPatterns = {
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624},  // 4097 with my C++ script
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 624, 624},  // 4098...
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 1248, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 624, 624, 624, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 624, 624, 1248, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 1248, 624, 624, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 1248, 624, 1248, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 624, 624, 624, 624, 624, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 624, 624, 624, 624, 1248, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 624, 624, 1248, 624, 624, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 624, 624, 1248, 624, 1248, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 1248, 624, 624, 624, 624, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 1248, 624, 624, 624, 1248, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 1248, 624, 1248, 624, 624, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 1248, 624, 1248, 624, 1248, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 624, 624, 624, 624, 624, 624, 624, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 624, 624, 624, 624, 624, 624, 1248, 624},
        {1248, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 624, 1248, 624, 624, 624, 624, 624, 1248, 624, 624, 624}  // 4114
    };


    private static HashMap<ImageButton, int[]> BUTTONS_PATTERNS_MAP = new HashMap<>();  // key is the button, its signal is value

    // Variables for debugging:
    private static final String TAG = "MainActivity";


    // ================================================================
    // System functions:

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Log.d(TAG, "onCreate: in");

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // ======================================================
        //Setting up View variables:


        // ========================
        // Setting up the buttons:

        // Setting the map of buttons(key) and their IR signals(value):
        BUTTONS_PATTERNS_MAP.put((ImageButton) findViewById(R.id.powerOnBtn), buttonsSignalPatterns[0]);
        BUTTONS_PATTERNS_MAP.put((ImageButton) findViewById(R.id.muteBtn), buttonsSignalPatterns[1]);
        BUTTONS_PATTERNS_MAP.put((ImageButton) findViewById(R.id.playPauseBtn), buttonsSignalPatterns[2]);
        BUTTONS_PATTERNS_MAP.put((ImageButton) findViewById(R.id.nextBtn), buttonsSignalPatterns[3]);
        BUTTONS_PATTERNS_MAP.put((ImageButton) findViewById(R.id.previousBtn), buttonsSignalPatterns[4]);


        // define on click listener for all the buttons:
        View.OnClickListener buttonPress = new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ImageButton curBtn = (ImageButton) view;
                btnEffect(curBtn);  // little blink
                transmitSignal(BUTTONS_PATTERNS_MAP.get(curBtn));
            }
        };

        // Set the on click listener for the buttons and manage their initial colours:
        for(Map.Entry kvPair : BUTTONS_PATTERNS_MAP.entrySet()) {
            ImageButton btn = (ImageButton) kvPair.getKey();
            btn.setOnClickListener(buttonPress);

            // Set the colours of all buttons:
            if(btn != (ImageButton) findViewById(R.id.powerOnBtn)) {  // normally coloured button
                btn.setColorFilter(Color.parseColor("#b0afaf"));  // set colour to grey
            } else {
                btn.setColorFilter(Color.parseColor("#800006"));  // if it is power on button set to red colour
            }
        }


        // ===========================
        // Setting up the seek bars:

        // Make this seekbar unclickable since its still(v0.4) disfunctional
        final SeekBar bassSeekBar = findViewById(R.id.bassSeekBar);
        bassSeekBar.setEnabled(false);

        final SeekBar playerVolumeSeekBar = findViewById(R.id.playerVolumeSeekBar);
        final SeekBar pcVolumeSeekBar = findViewById(R.id.pcVolumeSeekBar);


        // SeekBar listeners:
        SeekBar.OnSeekBarChangeListener seekbarChange = new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean fromUser) {
                // System.out.println("Progress changed to: "  + i);
                if (seekBar == pcVolumeSeekBar) {
                    transmitSignal(pcVolumeSignalPatterns[i]);
                } else {  // it is the playerVolumeSeekbar
                    transmitSignal(playerVolumeSignalPatterns[i]);
                }
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        };
        // Assign the listeners:
        playerVolumeSeekBar.setOnSeekBarChangeListener(seekbarChange);
        pcVolumeSeekBar.setOnSeekBarChangeListener(seekbarChange);


        Log.d(TAG, "onCreate: out");
    }
}
