package com.example.barcodereader.helpers.itemtouch;

import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.view.View;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.ItemTouchHelper;
import androidx.recyclerview.widget.RecyclerView;

public class SimpleItemTouchHelperCallBack extends ItemTouchHelper.Callback {

    private final ItemTouchHelperAdapter _adapter;
    public float ALPHA = 1.0f;

    public SimpleItemTouchHelperCallBack(ItemTouchHelperAdapter adapter) { _adapter = adapter; }

    @Override
    public boolean isLongPressDragEnabled() { return true; }

    @Override
    public boolean isItemViewSwipeEnabled() { return true; }

    @Override
    public int getMovementFlags(@NonNull RecyclerView recyclerView,
                                @NonNull RecyclerView.ViewHolder viewHolder) {
        int drag, swipe;

        if (recyclerView.getLayoutManager() instanceof GridLayoutManager) {
            drag = ItemTouchHelper.UP | ItemTouchHelper.DOWN| ItemTouchHelper.LEFT |
                    ItemTouchHelper.RIGHT;
            swipe = 0;
        } else {
            drag = ItemTouchHelper.UP | ItemTouchHelper.DOWN;
            swipe = ItemTouchHelper.START | ItemTouchHelper.END;
        }
        return makeMovementFlags(drag, swipe);
    }

    @Override
    public boolean onMove(@NonNull RecyclerView recyclerView,
                          @NonNull RecyclerView.ViewHolder vhSource,
                          @NonNull RecyclerView.ViewHolder vhTarget) {
        if (vhSource.getItemViewType() != vhTarget.getItemViewType()) {
            return false;
        } else {
            _adapter.onItemMove(vhSource.getAdapterPosition(), vhTarget.getAdapterPosition());
            return true;
        }
    }

    @Override
    public void onSwiped(@NonNull RecyclerView.ViewHolder viewHolder, int direction) {
        _adapter.onItemDismiss(viewHolder.getAdapterPosition());
    }

    @Override
    public void onChildDraw(@NonNull Canvas canvas, @NonNull RecyclerView recyclerView,
                            @NonNull RecyclerView.ViewHolder viewHolder,
                            float dX, float dY, int state, boolean isActive) {
        Paint paint = new Paint();

        if (state == ItemTouchHelper.ACTION_STATE_SWIPE) {
            float alpha = ALPHA - Math.abs(dX) / (float) viewHolder.itemView.getWidth();
            viewHolder.itemView.setAlpha(alpha);
            viewHolder.itemView.setTranslationX(dX);
            if (viewHolder.getAdapterPosition() == -1)
                return;

            paint.setColor(Color.RED);
            paint.setFakeBoldText(true);
            paint.setTextSize(50);
            paint.setTextAlign(Paint.Align.CENTER);

            View itemView = viewHolder.itemView;
            String inbox = "Delete";
            float x = itemView.getRight() - 200,
                    y = itemView.getTop() + (float)itemView.getHeight() / 2;

            canvas.drawText(inbox, x, y, paint);
        } else {
            super.onChildDraw(canvas, recyclerView, viewHolder, dX, dY, state, isActive);
        }
    }

    @Override
    public void onSelectedChanged(@Nullable RecyclerView.ViewHolder viewHolder, int state) {
        if (state != ItemTouchHelper.ACTION_STATE_IDLE &&
                viewHolder instanceof ItemTouchHelperViewHolder) {
            ItemTouchHelperViewHolder itemViewHolder = (ItemTouchHelperViewHolder) viewHolder;
            itemViewHolder.onItemSelected();
        }
        super.onSelectedChanged(viewHolder, state);
    }

    @Override
    public void clearView(@NonNull RecyclerView recyclerView,
                          @NonNull RecyclerView.ViewHolder viewHolder) {
        super.clearView(recyclerView, viewHolder);
        viewHolder.itemView.setAlpha(ALPHA);

        if (viewHolder instanceof ItemTouchHelperViewHolder) {
            ItemTouchHelperViewHolder itemViewHolder = (ItemTouchHelperViewHolder) viewHolder;
            itemViewHolder.onItemClear();
        }
    }

}
