package com.Shutdownify.app;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.example.httptest.R;

import org.json.JSONException;
import org.json.JSONObject;


public class MainActivity extends AppCompatActivity {


    public boolean demo_btn_status = true;
    public String HOST;
    public boolean device_state=false;
    //init stf
    EditText ipInput;
    EditText timeInp;
    TextView state_view;
    Button checkBtn;
    Button shutdownbtn;
    Button cancelbtn;
    CheckBox democheckBox;


    String TAG = "ANDORID_OUTPUT";


    @Override
    protected void onCreate(Bundle savedInstanceState) {


        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);



        checkBtn = findViewById(R.id.state_check_btn);
        democheckBox = findViewById(R.id.demo_checkBox);
        shutdownbtn = findViewById(R.id.shutdown_btn);
        cancelbtn=findViewById(R.id.cancel_button);
        ipInput = findViewById(R.id.ip_input_edittext);
        timeInp =findViewById(R.id.edit_Time);
        state_view= findViewById(R.id.state_view);
        democheckBox.setChecked(true);



        checkBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                demo_btn_status = democheckBox.isChecked();
                Log.d(TAG, "onClick: "+demo_btn_status);
                if (ipInput.getText().toString().isEmpty()) {
                    Toast.makeText(MainActivity.this, "Please enter IP address", Toast.LENGTH_SHORT).show();
                } else {
                    HOST = ipInput.getText().toString();
                    try {
                        init();

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        }

        );
        shutdownbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if (timeInp.getText().toString().isEmpty()) {
                    Toast.makeText(MainActivity.this, "Please enter time ", Toast.LENGTH_SHORT).show();
                } else {
                    HOST = ipInput.getText().toString();
                    try {
                        action("shutdown");

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
        );
        cancelbtn.setOnClickListener(new View.OnClickListener() {
                                         @Override
                                         public void onClick(View v) {
                                             try {
                                                 action("Cancel");
                                             } catch (JSONException e) {
                                                 e.printStackTrace();
                                             }
                                         }
                                     }
        );
    }
    private void action(String action) throws JSONException {
        demo_btn_status = democheckBox.isChecked();
        RequestQueue queue = Volley.newRequestQueue(this);
        String host = HOST + "/action";
        JSONObject jsonbody = new JSONObject();
        if(action.equals("Cancel")){
            jsonbody.put("Action", 0);
            jsonbody.put("Time", 0);
            jsonbody.put("Cancel", true);
        }else {
            jsonbody.put("Action", action);
            jsonbody.put("Time", timeInp.getText().toString());
            jsonbody.put("Cancel", false);
        }
        jsonbody.put("Demo_status", demo_btn_status);
        Log.d(TAG, "ONCLICK json req body "+ jsonbody);

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                host, jsonbody, new Response.Listener<JSONObject>() {

            @Override
            public void onResponse(JSONObject response) {

                Log.d(TAG, "onResponse: " + "working response "+response.toString()+" "+action);

                try {
                    //incase of error
                    if(response.has("Error")){
                        Toast.makeText(MainActivity.this, response.get("Error").toString(), Toast.LENGTH_SHORT).show();

                    }
                    // in case of cancel command
                    else if(response.has("STATUS") && response.get("STATUS").equals(false)){
                        Toast.makeText(MainActivity.this, "ALL ACTIVE COMMANDS CANCELED", Toast.LENGTH_SHORT).show();
                        Log.d(TAG, "onResponse: "+ "Cancel command "+response);
                        //in case of any other command
                    }else if (response.has("STATUS") && response.get("STATUS").equals(true) ){
                        cancelbtn.setEnabled(true);
                        Toast.makeText(MainActivity.this, "Device Will "+action+" in "+response.get("Time")+ " seconds", Toast.LENGTH_SHORT).show();
                        Log.d(TAG, "onResponse: "+ "command execs "+response);
                    }//in case of failure
                    else {
                        Toast.makeText(MainActivity.this, "Device is Either Offline", Toast.LENGTH_SHORT).show();
                        Log.d(TAG, "onResponse: failure "+response);
                        device_state = false;
                        cancelbtn.setEnabled(true);
                        state_view.setText("Device is Offline");
                        state_view.setBackgroundColor(getResources().getColor(R.color.red));
                        shutdownbtn.setEnabled(false);
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }


            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d(TAG, "onErrorResponse: " + "Fail  ");

                device_state = false;
                cancelbtn.setEnabled(true);
                state_view.setText("Device is Offline");
                state_view.setBackgroundColor(getResources().getColor(R.color.red));
                shutdownbtn.setEnabled(false);
                Toast.makeText(MainActivity.this, "DEVICE IS OFFLINE", Toast.LENGTH_SHORT).show();
            }
        });
        jsonObjReq.setRetryPolicy(new DefaultRetryPolicy(
                700,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        queue.add(jsonObjReq);
    }



    private void init( )throws JSONException  {
        RequestQueue queue = Volley.newRequestQueue(this);

        String host = HOST + "/init";

        JSONObject jsonObject = new JSONObject();
        jsonObject.put("Demo_status", demo_btn_status);
        Log.d(TAG, "onClick jsonbody: "+jsonObject);

        JsonObjectRequest jsonObjReq = new JsonObjectRequest(Request.Method.POST,
                host, jsonObject, new Response.Listener<JSONObject>() {

            @Override
            public void onResponse(JSONObject response) {

                Log.d(TAG, "onResponse:JSON Respons " +response.toString());
                if (response.has("STATE")) {
                    device_state = true;
                    Log.d(TAG, "init  "+true);
                    shutdownbtn.setEnabled(true);
                    state_view.setText("Device is Online");
                    state_view.setBackgroundColor(getResources().getColor(R.color.colorGreen));

                    Toast.makeText(MainActivity.this, "Device is Online ", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(MainActivity.this, "Device is Offline", Toast.LENGTH_SHORT).show();
                    device_state = false;
                    state_view.setText("Device is Offline");
                    state_view.setBackgroundColor(getResources().getColor(R.color.red));
                    shutdownbtn.setEnabled(false);
                }


            }
        }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d(TAG, "onResponse: " + "Fail  ");

                device_state = false;
                cancelbtn.setEnabled(true);
                state_view.setText("Device is Offline");
                state_view.setBackgroundColor(getResources().getColor(R.color.red));
                shutdownbtn.setEnabled(false);
                Toast.makeText(MainActivity.this, "DEVICE IS OFFLINE", Toast.LENGTH_SHORT).show();
            }
        });
        jsonObjReq.setRetryPolicy(new DefaultRetryPolicy(
                700,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        queue.add(jsonObjReq);
    }

}



