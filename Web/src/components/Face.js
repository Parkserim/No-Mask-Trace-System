import React, { useState, useEffect } from "react";
import axios from "axios";
import { Image, Form, TextArea, Grid, Button } from 'semantic-ui-react'

function Faces(props) {
    const [face, setFace] = useState([]);
    const [description, setDescription] = useState([]);

    useEffect(() => {
        const pk = props.match.params.pk
        let url = "/recognition/" + pk;
        axios
            .get(url)
            .then(({ data }) => {
                setFace(data)
                setDescription(data.description)
            });
    }, [props.match.params.pk]);

    const onChangeValue = (e) => {
        setDescription(e.target.value)
    }

    const onRevice = () => {
        axios
            .patch("/recognition/" + face.pk, {
                "description": description,
            })
    }

    return (
        <Grid >
            <Grid.Row>
                <Grid.Column width={2}>
                    <Image src={face.image} />
                </Grid.Column>
                <Grid.Column width={14} className="text-right">
                    <Button id={face.pk} onClick={onRevice} size="mini" basic color="blue">수정</Button>
                    <hr></hr>
                    <Form>
                        <TextArea value={description} onChange={onChangeValue} />
                    </Form>
                </Grid.Column>
            </Grid.Row>
        </Grid >
    );
}

export default Faces;
