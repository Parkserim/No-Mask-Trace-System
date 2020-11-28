import React, { useState } from "react";
import axios from "axios";
import { Grid, Segment } from 'semantic-ui-react';
import { useHistory } from 'react-router-dom'
function DeviceCreate() {
    const [location, setLocation] = useState("");
    const [sublocation, setSubLocation] = useState("");
    const history = useHistory();

    // 검색 버튼 클릭시
    const onSubmit = (e) => {
        e.preventDefault();
        const url = "/devices/"
        axios
            .post(url, { "location": { location }.location, "sublocation": { sublocation }.sublocation })
            .then(({ data }) => {
                history.goBack();
            }).catch((err) => {
                const status = err.response.status
                if (status === 412) {
                    alert("이미 존재하는 시리얼 번호입니다.")
                    setSubLocation("")
                    setLocation("")
                }
            });
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
    return (
        < Grid.Column >
            <Segment>
                <div style={{ height: "20rem", marginTop: "8rem" }}>
                    <h1 style={{ textAlign: "center" }}>Device Create</h1>
                    <form onSubmit={onSubmit} style={{ textAlign: "center" }}>
                        <div className="form-row" style={{ marginTop: "3rem" }}>
                            <div className="form-group col-md-3">
                            </div>
                            <div className="form-group col-md-3">
                                <input onChange={onChangeValue} value={location} className="form-control" name="location" type="text" placeholder="location" />
                            </div>
                            <div className="form-group col-md-3">
                                <input onChange={onChangeValue} value={sublocation} className="form-control" name="sublocation" type="text" placeholder="sublocation" />
                            </div>
                            <div className="form-group col-md-2">
                                <input className="btn btn-outline-secondary" type="submit" value="Create" />
                            </div>
                        </div>
                    </form>
                </div>
            </Segment>
        </Grid.Column >
    );
}

export default DeviceCreate;
