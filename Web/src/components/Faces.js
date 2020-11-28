import React, { useState, useEffect } from "react";
import axios from "axios";
import { Table, Segment } from 'semantic-ui-react'
import { Link } from "react-router-dom";

function Faces() {
    const [faces, setFaces] = useState([]);
    useEffect(() => {
        let url = "/recognition/";
        axios
            .get(url)
            .then(({ data }) => {
                setFaces(data)
            });
    }, []);
    return (
        <Segment style={{ margin: "auto" }}>
            <Table celled>
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell width={2} className="text-center">Identity Number</Table.HeaderCell>
                        <Table.HeaderCell width={12} className="text-center">Description</Table.HeaderCell>
                        <Table.HeaderCell width={2} className="text-center">Image</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {faces.map(face => (
                        <Table.Row key={face.pk}>
                            <Table.Cell className="text-center">{face.pk}</Table.Cell>
                            <Table.Cell className="text-center">{face.description}</Table.Cell>
                            <Table.Cell className="text-center"><Link to={'/face/' + face.pk}>Click</Link></Table.Cell>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table>
        </Segment >
    );
}


export default Faces;
