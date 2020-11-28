import React, { useState, useEffect } from "react";
import axios from "axios";
import { Pagination, Segment, Button } from 'semantic-ui-react';
import { Link } from "react-router-dom";



function Devices() {
    const [devices, setDevices] = useState([]);
    const [page, setPage] = useState(1);
    const [totalPage, setTotalPage] = useState(0);
    // eslint-disable-next-line
    const loadDevices = (page) => {
        axios
            .get("/devices/?page=" + page,)
            .then(({ data }) => {
                setDevices(data.results)
                let count = data.count
                const PAGE_SIZE = 10
                setTotalPage(Math.ceil(count / PAGE_SIZE))
            });
    }

    useEffect(() => {
        loadDevices(page);
        // eslint-disable-next-line
    }, [page]);

    const onDelete = (e) => {
        const pk = e.target.id
        var flag = window.confirm("정말 삭제하시겠습니까?");
        if (flag) {
            axios
                .delete("/devices/" + pk)
                .then(() => {
                    loadDevices();
                });
        }
    }
    const onRevice = (pk, location, sublocation) => {
        var prompt_location = window.prompt("수정할 Location 값을 입력하세요", location)
        var prompt_sublocation = window.prompt("수정할 SubLocation 값을 입력하세요", sublocation)

        axios
            .put("/devices/" + pk, {
                "location": prompt_location, "sublocation": prompt_sublocation,
            }
            )
            .then(() => {
                loadDevices();
            });

    }
    const onPageChange = (e, pageInfo) => {
        setPage(pageInfo.activePage)
    }
    return (
        <Segment style={{ margin: "auto" }}>
            <div style={{ marginTop: "3rem" }}>
                {/* <h1 style={{ textAlign: "center" }}>Device List</h1> */}
                <div style={{ textAlign: "right" }}>
                    <button className="btn btn-outline-secondary"><Link to={'/device_create/'}>Create</Link></button>
                </div>
                <table className="table " style={{ marginTop: "1rem" }}>
                    <thead className="thead-dark">
                        <tr>
                            <th style={{ width: "40%" }} className="text-center">Location</th>
                            <th style={{ width: "40%" }} className="text-center">SubLocation</th>
                            <th style={{ width: "20%" }}></th>
                        </tr>
                    </thead>
                    <tbody>
                        {devices.map(device => (
                            <tr key={device.pk}>
                                <td style={{ width: "40%" }} className="text-center"> {device.location}</td>
                                <td style={{ width: "40%" }} className="text-center">{device.sublocation}</td>
                                <td style={{ width: "20%" }} className="text-right">
                                    <Button id={device.pk} onClick={onDelete} size="mini" basic color="red">삭제</Button>
                                    <Button id={device.pk} onClick={() => onRevice(device.pk, device.location, device.sublocation)} size="mini" basic color="blue">수정</Button>
                                </td>
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
            </div >
        </Segment >
    );
}

export default Devices;
