import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

class Dialog extends React.Component {

    constructor(props){
        super(props);

        this.state = {
            show: this.props.show
        };
    }

    render() {
        const submitText = this.props.submitText ? this.props.submitText : 'Submit';

        return (
            <Modal centered={true} show={this.props.show} onHide={this.props.hideModal}>
                <Modal.Header closeButton>
                    <Modal.Title>{this.props.title}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {this.props.children}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="primary" onClick={this.props.onSubmit}>{submitText}</Button>
                    <Button variant="secondary" onClick={this.props.hideModal}>Cancel</Button>
                </Modal.Footer>
            </Modal>
        );
    }

}

export default Dialog;