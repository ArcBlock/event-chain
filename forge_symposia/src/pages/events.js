/* eslint-disable react/jsx-one-expression-per-line */

import React from 'react';
import styled from 'styled-components';

import moment from 'moment';

import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import CalendarToday from '@material-ui/icons/CalendarToday';
import LocationOn from '@material-ui/icons/LocationOn';

import api from '../libs/api';
import Layout from '../components/layout';
import useAsync from 'react-use/lib/useAsync';
import CircularProgress from '@material-ui/core/CircularProgress/CircularProgress';
import PageHeader from '../components/page_header';

async function fetchEventList() {
  return await Promise.all([api.get('/api/list_events')]);
}

const renderEvents = events => {
  return (
    <Grid container spacing={5}>
      {events.map((event, index) => {
        const detailPath = `detail?event_address=${event.address}`;
        return (
          <Grid item xs={4} key={`${event.title}-${index}`}>
            <Card key={event.title}>
              <a href={detailPath} alt={event.title}>
                <CardMedia
                  style={{ height: 230 }}
                  image={event.img_url}
                  title={event.title}
                />
              </a>
              <CardContent className="event-content">
                <Typography
                  gutterBottom
                  variant="h5"
                  component="a"
                  href={detailPath}
                >
                  <span>{event.title}</span>
                </Typography>
                <div className="details">
                  <Typography color="textSecondary" component="p">
                    <LocationOn /> {event.location}
                  </Typography>
                  <Typography color="textSecondary" component="p">
                    <CalendarToday />{' '}
                    <span>
                      {moment(event.start_time).format('dd, MMM DD, YYYY')}
                    </span>
                  </Typography>
                </div>
                <hr />
                <nav className="level">
                  <div className="level-item has-text-centered">
                    <div>
                      <p className="heading">Tickets</p>
                      <p className="title">
                        {event.num_created}/{event.limit}
                      </p>
                    </div>
                  </div>
                  <div className="level-item has-text-centered">
                    <div>
                      <p className="heading">Price</p>
                      <p className="title">{event.price} TBA</p>
                    </div>
                  </div>
                </nav>
              </CardContent>
              <CardActions className="footer">
                <Button
                  component="a"
                  href={detailPath}
                  color="primary"
                  fullWidth
                >
                  Details
                </Button>
              </CardActions>
            </Card>
          </Grid>
        );
      })}
    </Grid>
  );
};

export default function EventsPage() {
  const state = useAsync(fetchEventList);

  if (state.loading || !state.value) {
    return (
      <Layout title="Events">
        <Main>
          <CircularProgress />
        </Main>
      </Layout>
    );
  }

  if (state.error) {
    return (
      <Layout title="Payment">
        <Main>{state.error.message}</Main>
      </Layout>
    );
  }
  const eventList = state.value[0].data;

  return (
    <Layout title="Home">
      <Main>
        <PageHeader title="Welcome to Forge Symposia!" />
        {renderEvents(eventList)}
      </Main>
    </Layout>
  );
}
const Main = styled.main`
  hr {
    background-color: #ecf0f1;
    border: none;
    display: block;
    height: 2px;
    margin: 1.5rem 0;
  }

  a {
    color: ${props => props.theme.colors.green};
    text-decoration: none;
  }

  .event-content {
    padding: 1.5rem;
    background-color: #fafafa;

    .details {
      margin-top: 1.5rem;
    }

    .details > p {
      display: flex;
      align-items: center;
    }

    .details > p > svg {
      margin-right: 0.5rem;
    }

    .level {
      display: flex;
      align-items: center;
      justify-content: space-between;

      .level-item:not(.is-narrow) {
        flex-grow: 1;
      }
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

    .heading {
      display: block;
      font-size: 11px;
      letter-spacing: 1px;
      margin-bottom: 5px;
      text-transform: uppercase;
    }

    .title {
      color: #363636;
      font-size: 2rem;
      font-weight: 500;
      line-height: 1.125;
    }
  }

  .footer {
    padding: 0;
    height: 4rem;
    background-color: rgba(236, 240, 241, 0.8);

    * {
      height: 100%;
      font-size: 1rem;
    }
  }

  .event-content p:not(:last-child) {
    margin-bottom: 1rem;
  }
`;
