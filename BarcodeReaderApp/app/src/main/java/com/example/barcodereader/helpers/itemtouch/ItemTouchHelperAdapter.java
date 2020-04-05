package com.example.barcodereader.helpers.itemtouch;

public interface ItemTouchHelperAdapter {

    void onItemDismiss(int position);
    boolean onItemMove(int from, int to);

}
