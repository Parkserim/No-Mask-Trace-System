import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import DateRangePicker from '@wojtekmaj/react-daterange-picker';
import { Pagination, Segment } from 'semantic-ui-react';
// import { applyMiddleware } from "redux";



function Files() {
  const [files, setFiles] = useState([]);
  const [location, setLocation] = useState("");
  const [sublocation, setSubLocation] = useState("");
  const [page, setPage] = useState(1);
  const [totalPage, setTotalPage] = useState(0);
  const [date, setDates] = useState([new Date("1900/01/01"), new Date("2099/12/31")]);

  const loadFiles = (page) => {
    let start_date = { date }.date[0]
    let end_date = { date }.date[1]
    let first_date = start_date.getFullYear() + "-" + (Number(start_date.getMonth()) + Number(1)) + "-" + start_date.getDate()
    let second_date = end_date.getFullYear() + "-" + (Number(end_date.getMonth()) + Number(1)) + "-" + end_date.getDate()
    let url = "/files/?location=" + { location }.location + "&sublocation=" + { sublocation }.sublocation + "&min_created_at=" + first_date + "+&max_created_at=" + second_date + "&page=" + page

    axios
      .get(url)
      .then(({ data }) => {
        setFiles(data.results)
        let count = data.count
        const PAGE_SIZE = 10
        setTotalPage(Math.ceil(count / PAGE_SIZE))
      });
  }
  // 페이지 접속 시
  useEffect(() => {
    loadFiles(page)
    // eslint-disable-next-line
  }, [page]);

  // 검색 버튼 클릭시
  const onSubmit = (e) => {
    e.preventDefault();
    loadFiles({ page }.page)
  }
  // pagination 버튼 클릭 시
  const onPageChange = (e, pageInfo) => {
    setPage(pageInfo.activePage)
  }

  // input tag value 변화시
  const onChangeValue = (e) => {
    let name = e.target.name
    if (name === "sublocation") {
      setSubLocation(e.target.value)
    }
    if (name === "location") {
      setLocation(e.target.value)
    }
  }
  const onChangeDate = (e) => {
    setDates(e)
  }

  return (
    <Segment style={{ margin: "auto" }}>
      <div>
        {/* <h1 style={{ textAlign: "center" }}>File List</h1> */}
        <form onSubmit={onSubmit} style={{ textAlign: "center" }}>
          <div className="form-row" style={{ marginTop: "3rem" }}>
            <div className="form-group col-md-4">
              <DateRangePicker
                onChange={onChangeDate}
                value={date}
              />
            </div>
            <div className="form-group col-md-3">
              <input onChange={onChangeValue} className="form-control" name="location" type="text" placeholder="location" />
            </div>
            <div className="form-group col-md-3">
              <input onChange={onChangeValue} className="form-control" name="sublocation" type="text" placeholder="sublocation" />
            </div>
            <div className="form-group col-md-1">
              <input className="btn btn-outline-secondary" type="submit" value="검색" />
            </div>
          </div>
        </form>
        <table className="table  " style={{ marginTop: "1rem" }}>
          <thead className="thead-dark">
            <tr>
              <th style={{ width: "30%" }} className="text-center">Location</th>
              <th style={{ width: "30%" }} className="text-center">SubLocation</th>
              <th style={{ width: "20%" }} className="text-center">Created</th>
              <th style={{ width: "20%" }} className="text-center">Image</th>
            </tr>
          </thead>
          <tbody>
            {files.map(file => (
              <tr key={file.pk}>
                <td className="text-center">{file.location}</td>
                <td className="text-center">{file.sublocation}</td>
                <td className="text-center">{file.created_at}</td>
                <td className="text-center"><Link to={'/detail/' + file.pk}>Click</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
        <div style={{ textAlign: "center" }}>
          <Pagination
            boundaryRange={5}
            defaultActivePage={1}
            ellipsisItem={null}
            firstItem={null}
            lastItem={null}
            siblingRange={1}
            totalPages={totalPage}
            onPageChange={onPageChange}
          />
        </div>
      </div>
    </Segment>


  );
}

export default Files;
