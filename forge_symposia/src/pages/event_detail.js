/* eslint-disable react/jsx-one-expression-per-line */
import React from 'react';
import styled from 'styled-components';
import useAsync from 'react-use/lib/useAsync';

import useToggle from 'react-use/lib/useToggle';
import Typography from '@material-ui/core/Typography';
import LocationOn from '@material-ui/icons/LocationOn';
import CalendarToday from '@material-ui/icons/CalendarToday';
import HourglassEmpty from '@material-ui/icons/HourglassEmpty';
import CircularProgress from '@material-ui/core/CircularProgress/CircularProgress';

import moment from 'moment';
import qs from 'querystring';
import Auth from '@arcblock/react-forge/lib/Auth';

import api from '../libs/api';
import Layout from '../components/layout';
import { onAuthError } from '../libs/auth';
import { Grid, Button } from '@material-ui/core';
import Ticket from '../components/ticket';

async function fetchEventDetail(event_address) {
  return await api.get(`/api/detail/${event_address}`);
}

export default function EventDetailPage() {
  const params = qs.parse(window.location.search.slice(1));
  const state = useAsync(() => fetchEventDetail(params.event_address));
  const [open, toggle] = useToggle(false);

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
  const event = state.value.data;

  return (
    <Layout title="Home">
      <Main>
        <div className="card-header">
          <img
            style={{ width: '100%', height: '540px' }}
            src={event.img_url}
            alt={event.title}
          />
        </div>
        <Grid container className="card-content">
          <Grid item xs={8}>
            <Typography variant="h3">{event.title}</Typography>
            <Typography className="subtitle" variant="subtitle1">
              Created by XXX ( Account: {event.issuer} )
            </Typography>
            <Typography className="content" variant="body1">
              {event.details}
            </Typography>
          </Grid>
          <Grid item xs={4}>
            <Grid item>
              <Ticket
                price={event.price}
                numCreated={event.num_created}
                limit={event.limit}
              />
              <hr />
            </Grid>
            <Grid item className="date-geo">
              <Typography color="textSecondary" component="p">
                <LocationOn /> {event.location}
              </Typography>
              <Typography color="textSecondary" component="p">
                <CalendarToday />{' '}
                <span>
                  {moment(new Date(event.start_time)).format('dd, MMM DD, YYYY')}
                </span>
              </Typography>
              <Typography color="textSecondary" component="p">
                <HourglassEmpty />{' '}
                <span>{moment(new Date(event.end_time)).format('dd, MMM DD, YYYY')}</span>
              </Typography>
            </Grid>
            <Grid item className="action">
              <Button variant="contained" color="primary" fullWidth>
                Buy Ticket
              </Button>
              <Button variant="contained" color="primary" fullWidth>
                Join Event
              </Button>
            </Grid>
          </Grid>
        </Grid>
      </Main>
      {open && (
        <Auth
          responsive
          extraParams={{ event_address: params.event_address }}
          action="buy_ticket"
          checkFn={api.get}
          onError={onAuthError}
          onClose={() => toggle()}
          onSuccess={() => window.location.reload()}
          messages={{
            title: 'Payment Required',
            scan: 'Pay to buy ticket for this event',
            confirm: 'Confirm payment on your ABT Wallet',
            success: 'You have successfully paid!',
          }}
        />
      )}
    </Layout>
  );
}
const Main = styled.main`
  a {
    color: ${props => props.theme.colors.green};
    text-decoration: none;
  }

  .card-header {
    img {
      width: 100%;
      height: 0.6rem;
      border-radius: 0.4rem 0.4rem 0 0;
    }
  }

  .card-content {
    margin-top: 1.5rem;
    padding: 1.5rem;

    h3 {
      font-size: 2.5rem;
    }

    .subtitle {
      margin-top: 10px;
    }

    .date-geo {
      margin-top: 1.5rem;
    }

    .date-geo > p {
      display: flex;
      align-items: center;

      :not(:last-child) {
        margin-bottom: 1rem;
      }
    }

    .date-geo > p > svg {
      margin-right: 0.5rem;
    }

    .action {
      margin-top: 1.5rem;
    }

    .action> button: not(: last-child) {
      margin-bottom: 1.5rem;
    }
  }

  hr {
    background-color: #ecf0f1;
    border: none;
    display: block;
    height: 2px;
  }
`;
