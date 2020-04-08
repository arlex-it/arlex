package com.example.barcodereader.helpers.model;

import androidx.room.Dao;
import androidx.room.Query;

import com.example.barcodereader.helpers.constant.TableNames;
import com.example.barcodereader.helpers.util.database.BaseDao;

import java.util.List;

import io.reactivex.Flowable;

@Dao
public interface CodeDAO extends BaseDao<Code> {

    @Query("SELECT * FROM " + TableNames.CODES)
    Flowable<List<Code>> getAllFlowableCodes();

}
