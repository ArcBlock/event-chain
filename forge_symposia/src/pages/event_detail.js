/* eslint-disable react/jsx-one-expression-per-line */

import React from 'react';
import styled from 'styled-components';

import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import useToggle from 'react-use/lib/useToggle';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';

import Layout from '../components/layout';
import api from '../libs/api';
import useAsync from 'react-use/lib/useAsync';
import CircularProgress from '@material-ui/core/CircularProgress/CircularProgress';
import qs from 'querystring';
import Auth from '@arcblock/react-forge/lib/Auth';
import { onAuthError } from '../libs/auth';
import PageHeader from '../components/page_header';

async function fetchEventDetail(event_address) {
  return await api.get(`/api/detail/${event_address}`);
}

export default function EventDetailPage() {
  const params = qs.parse(window.location.search.slice(1));
  const state = useAsync(() => fetchEventDetail(params.event_address));
  const [open, toggle] = useToggle(false);
  const [consume_open, consume_toggle] = useToggle(false);

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
  const x = state.value.data;

  return (
    <Layout title="Home">
      <Main>
        <PageHeader title={x.title} />
        <Card key={x.title} className="demo">
          <CardMedia className="event-pic" image={x.img_url} title={x.title} />
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
              {x.title}
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              Start Time: {x.start_time}
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              Location: {x.location}
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              Details: {x.details}
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              Availiable Tickets: {x.limit - x.num_created}/{x.limit}
            </Typography>
          </CardContent>
          <CardActions>
            <Button
              component="a"
              onClick={() => toggle()}
              size="small"
              color="primary"
            >
              Buy Ticket
            </Button>
            <Button
              component="a"
              onClick={() => consume_toggle()}
              size="small"
              color="primary"
            >
              Use Ticket
            </Button>
          </CardActions>
        </Card>
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
      {consume_open && (
        <Auth
          responsive
          extraParams={{ event_address: params.event_address }}
          action="consume_ticket"
          checkFn={api.get}
          onError={onAuthError}
          onClose={() => consume_toggle()}
          onSuccess={() => window.location.reload()}
          messages={{
            title: 'Select a ticket to use',
            scan: 'Confirm to use the ticket',
            confirm: 'Confirm to use this ticket',
            success: 'You have confirmed to use the ticket!',
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

  .demos {
    display: flex;
    justify-content: space-between;
    dalign-items: center;

    .demo {
      width: 30%;
    }
  }
  .event-pic {
    height: 540px;
  }
`;
