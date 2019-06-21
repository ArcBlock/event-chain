import React from 'react';

import PropTypes from 'prop-types';
import styled from 'styled-components';

export default function Ticket({ limit, numCreated, price }) {
  return (
    <Main>
      <nav className="level">
        <div className="level-item has-text-centered">
          <div>
            <p className="heading">Tickets</p>
            <p className="title">
              {numCreated}/{limit}
            </p>
          </div>
        </div>
        <div className="level-item has-text-centered">
          <div>
            <p className="heading">Price</p>
            <p className="title">{price} TBA</p>
          </div>
        </div>
      </nav>
    </Main>
  );
}

Ticket.propTypes = {
  limit: PropTypes.number,
  numCreated: PropTypes.number,
  price: PropTypes.number,
};

const Main = styled.main`
  margin-bottom: -1.5rem;

  .level {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 2rem;

    .level-item:not(.is-narrow) {
      flex-grow: 1;
    }
  }

  .heading {
    display: block;
    font-size: 11px;
    letter-spacing: 1px;
    margin-bottom: 5px;
    text-transform: uppercase;
  }

  .level-item {
    align-items: center;
    display: flex;
    flex-basis: auto;
    flex-grow: 0;
    flex-shrink: 0;
    justify-content: center;
  }

  .has-text-centered {
    text-align: center !important;
  }
`;
