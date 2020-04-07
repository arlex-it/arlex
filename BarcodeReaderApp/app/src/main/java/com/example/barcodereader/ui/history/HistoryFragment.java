package com.example.barcodereader.ui.history;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.databinding.DataBindingUtil;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DefaultItemAnimator;
import androidx.recyclerview.widget.ItemTouchHelper;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.barcodereader.R;
import com.example.barcodereader.databinding.FragmentHistoryBinding;
import com.example.barcodereader.helpers.constant.IntentKey;
import com.example.barcodereader.helpers.itemtouch.OnStartDragListener;
import com.example.barcodereader.helpers.itemtouch.SimpleItemTouchHelperCallBack;
import com.example.barcodereader.helpers.model.Code;
import com.example.barcodereader.helpers.util.ProgressDialogUtil;
import com.example.barcodereader.helpers.util.database.DatabaseUtil;
import com.example.barcodereader.ui.base.ItemClickListener;
import com.example.barcodereader.ui.scanresult.ScanResultActivity;

import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.CompositeDisposable;
import io.reactivex.schedulers.Schedulers;

public class HistoryFragment extends Fragment implements OnStartDragListener, ItemClickListener<Code> {

    private Context _context;
    private FragmentHistoryBinding _binding;
    private CompositeDisposable _compositeDisposable;
    private ItemTouchHelper _itemTouchHelper;
    private HistoryAdapter _adapter;

    private CompositeDisposable getCompositeDisposable() {
        return _compositeDisposable;
    }

    private void setCompositeDisposable(CompositeDisposable compositeDisposable) {
        _compositeDisposable = compositeDisposable;
    }

    public HistoryFragment() {}

    public static HistoryFragment newInstance() {
        return new HistoryFragment();
    }

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        _binding = DataBindingUtil.inflate(inflater, R.layout.fragment_history, container, false);
        return _binding.getRoot();
    }

    @Override
    public void onAttach(Context context) {
        super.onAttach(context);
        _context = context;
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        if (_context != null) {
            _binding.recyclerViewHistory.setLayoutManager(new LinearLayoutManager(_context));
            _binding.recyclerViewHistory.setItemAnimator(new DefaultItemAnimator());
            _adapter = new HistoryAdapter(this);
            _binding.recyclerViewHistory.setAdapter(_adapter);
            ItemTouchHelper.Callback callback = new SimpleItemTouchHelperCallBack(_adapter);
            _itemTouchHelper = new ItemTouchHelper(callback);
            _itemTouchHelper.attachToRecyclerView(_binding.recyclerViewHistory);
        }
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setCompositeDisposable(new CompositeDisposable());

        if (_context == null) {
            return;
        }

        ProgressDialogUtil.on().showProgressDialog(_context);
        getCompositeDisposable().add(DatabaseUtil.on().getAllCodes().observeOn(AndroidSchedulers.mainThread())
                .subscribeOn(Schedulers.io()).subscribe(codeList -> {
                    if (codeList.isEmpty()) {
                        _binding.imageViewEmptyBox.setVisibility(View.VISIBLE);
                        _binding.textViewNoItemPlaceholder.setVisibility(View.VISIBLE);
                    } else {
                        _binding.textViewNoItemPlaceholder.setVisibility(View.GONE);
                        _binding.imageViewEmptyBox.setVisibility(View.INVISIBLE);
                    }

                    getAdapter().clear();
                    getAdapter().addItem(codeList);
                    ProgressDialogUtil.on().hideProgressDialog();
                }, e -> ProgressDialogUtil.on().hideProgressDialog()));
    }

    private HistoryAdapter getAdapter() {
        return (HistoryAdapter) _binding.recyclerViewHistory.getAdapter();
    }

    @Override
    public void onStartDrag(RecyclerView.ViewHolder viewHolder) {
        _itemTouchHelper.startDrag(viewHolder);
    }

    @Override
    public void onItemClick(View view, Code item, int position) {
        Intent intent = new Intent(_context, ScanResultActivity.class);
        intent.putExtra(IntentKey.MODEL, item);
        intent.putExtra(IntentKey.IS_HISTORY, true);
        startActivity(intent);
    }
}
