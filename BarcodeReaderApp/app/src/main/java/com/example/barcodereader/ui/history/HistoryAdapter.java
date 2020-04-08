package com.example.barcodereader.ui.history;

import android.content.Context;
import android.os.AsyncTask;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.databinding.DataBindingUtil;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;
import com.bumptech.glide.request.RequestOptions;
import com.example.barcodereader.R;
import com.example.barcodereader.databinding.ItemHistoryBinding;
import com.example.barcodereader.helpers.constant.AppConstants;
import com.example.barcodereader.helpers.itemtouch.ItemTouchHelperAdapter;
import com.example.barcodereader.helpers.model.Code;
import com.example.barcodereader.helpers.util.TimeUtil;
import com.example.barcodereader.helpers.util.database.DatabaseUtil;
import com.example.barcodereader.ui.base.ItemClickListener;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class HistoryAdapter extends RecyclerView.Adapter<HistoryAdapter.HistoryViewHolder> implements ItemTouchHelperAdapter {

    private List<Code> _itemList;
    private ItemClickListener<Code> _itemClickListener;

    public HistoryAdapter(ItemClickListener<Code> itemClickListener) {
        _itemList = new ArrayList<>();
        _itemClickListener = itemClickListener;
    }

    private boolean isEqual(Code left, Code right) {
        //return left.equals(right);
        return false;
    }

    public void clear() {
        _itemList.clear();
        notifyDataSetChanged();
    }

    public void setItemList(List<Code> itemList) {
        _itemList = itemList;
    }

    public List<Code> getItems() {
        return _itemList;
    }

    public void removeItem(Code item) {
        int index = getItemPosition(item);
        if (index < 0 || index >= _itemList.size()) {
            return;
        }
        _itemList.remove(index);
        notifyItemRemoved(index);
    }

    public Code getItem(int position) {
        if (position < 0 || position >= _itemList.size()) {
            return null;
        }
        return _itemList.get(position);
    }

    public int getItemPosition(Code item) {
        return _itemList.indexOf(item);
    }

    public int addItem(Code item) {
        Code oldItem = findItem(item);

        if (oldItem == null) {
            _itemList.add(item);
            notifyItemInserted(_itemList.size() - 1);
            return _itemList.size() - 1;
        }
        return updateItem(item, item);
    }

    public void addItem(List<Code> items) {
        for (Code item : items) {
            addItem(item);
        }
    }

    public void addItemToPosition(Code item, int position) {
        _itemList.add(position, item);
        notifyItemInserted(position);
    }

    public void addItemToPosition(List<Code> item, int position) {
        _itemList.addAll(position, item);
        notifyItemRangeChanged(position, item.size());
    }

    public Code findItem(Code item) {
        for (Code currentItem : _itemList) {
            if (isEqual(item, currentItem)) {
                return currentItem;
            }
        }
        return null;
    }

    public int updateItem(Code oldItem, Code newItem) {
        int oldItemIndex = getItemPosition(oldItem);
        _itemList.set(oldItemIndex, newItem);
        notifyItemChanged(oldItemIndex);
        return oldItemIndex;
    }

    public int updateItem(Code newItem, int position) {
        _itemList.set(position, newItem);
        notifyItemChanged(position);
        return position;
    }

    @Override
    public int getItemCount() {
        return _itemList.size();
    }

    @NonNull
    @Override
    public HistoryViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        return new HistoryViewHolder(DataBindingUtil.inflate(LayoutInflater.from(parent.getContext()),
                R.layout.item_history, parent, false));
    }

    @Override
    public void onBindViewHolder(@NonNull HistoryViewHolder holder, int position) {
        Code item = getItem(position);
        if (item != null) {
            holder.bind(item);
        }
    }

    @Override
    public boolean onItemMove(int fromPosition, int toPosition) {
        // should delete item if it moves
        return false;
    }

    @Override
    public void onItemDismiss(int position) {
        AsyncTask.execute(() -> {
            DatabaseUtil.on().deleteEntity(getItem(position));
            _itemList.remove(position);
        });
    }

    class HistoryViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {

        private ItemHistoryBinding _itemHistoryBinding;

        HistoryViewHolder(@NonNull ItemHistoryBinding itemHistoryBinding) {
            super(itemHistoryBinding.getRoot());
            _itemHistoryBinding = itemHistoryBinding;
        }

        void bind(Code item) {
            Context context = _itemHistoryBinding.getRoot().getContext();

            if (context != null) {
                Glide.with(context).asBitmap().apply(new RequestOptions()
                        .skipMemoryCache(false).diskCacheStrategy(DiskCacheStrategy.ALL))
                        .load(item.getImagePath()).into(_itemHistoryBinding.imageViewCode);

                String scanType = String.format(Locale.ENGLISH, context.getString(R.string.code_scan),
                        context.getResources().getStringArray(R.array.code_types)[item.getType()]);

                _itemHistoryBinding.textViewCodeType.setText(scanType);
                _itemHistoryBinding.textViewTime.setText(TimeUtil.getFormattedDateString(
                        item.getTimestamp(),
                        AppConstants.APP_HISTORY_DATE_FORMAT));
            }

            _itemHistoryBinding.constraintLayoutContainer.setOnClickListener(this);
        }

        @Override
        public void onClick(View v) {
            if (_itemClickListener != null) {
                _itemClickListener.onItemClick(v, getItem(getAdapterPosition()), getAdapterPosition());
            }
        }
    }
}
