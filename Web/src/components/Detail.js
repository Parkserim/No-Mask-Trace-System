import React, { useState, useEffect } from "react";
import axios from "axios";
import { Grid, Segment } from 'semantic-ui-react';

function Detail(props) {
  const [post, setPosts] = useState([]);

  useEffect(() => {
    const pk = props.match.params.pk
    axios
      .get("/files/" + pk,)
      .then(({ data }) => setPosts(data));
  }, [props.match.params.pk]);

  return (
    <Grid.Column stretched width={16}>
      <Segment style={{ margin: "auto", backgroundColor: "lightgray" }}>
        <div>
          <div className="card">
            <div className="row no-gutters">
              <div className="col-md-7">
                <img src={post.image} alt="" className="card-img" />
              </div>
              <div className="col-md-5 " style={{ margin: "auto" }}>
                <div className="card-body" >
                  <p className="card-text" style={{ fontSize: "18px", textAlign: "center" }}>
                    <strong>
                      PK : {post.pk}<br></br><br></br>
                      Created : {post.created_at}<br></br><br></br>
                      Location : {post.location}<br></br><br></br>
                      SubLocation : {post.sublocation}<br></br><br></br>
                    </strong>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Segment>
    </Grid.Column>

  );
}

export default Detail;
