import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';
import Chatbot from '../components/Chatbot';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">
          Welcome to the comprehensive guide for building AI-driven robotics solutions. Explore the modules below to dive into ROS 2, Digital Twins, NVIDIA Isaac, and Vision-Language-Action systems.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/ros2-initial/spec-v1">
            Start Reading
          </Link>
        </div>
      </div>
    </header>
  );
}

function HomepageModules() {
  const modules = [
    {
      title: 'Module 1: ROS 2 Fundamentals (Initial)',
      description: 'An early specification exploring ROS 2 basics for humanoid robot control.',
      link: '/docs/ros2-initial/spec-v1',
    },
    {
      title: 'Module 1: ROS 2 & RAG Chatbot (Refined)',
      description: 'A comprehensive plan for an AI-Native Book on ROS 2 with an integrated RAG Chatbot.',
      link: '/docs/ros2-refined/spec-v2',
    },
    {
      title: 'Module 2: The Digital Twin',
      description: 'Learn about creating digital twins for humanoid robots using Gazebo and Unity.',
      link: '/docs/digital-twin/spec',
    },
    {
      title: 'Module 3: AI-Robot Brain - NVIDIA Isaac',
      description: 'Dive into advanced perception, VSLAM, and navigation using NVIDIA Isaac Sim and Isaac ROS.',
      link: '/docs/isaac-brain/spec',
    },
    {
      title: 'Module 4: Vision-Language-Action (VLA)',
      description: 'Explore voice-to-action systems, cognitive planning, and full integration for autonomous humanoids.',
      link: '/docs/vla-module/spec',
    },
  ];

  return (
    <section className={styles.modules}>
      <div className="container">
        <div className="row">
          {modules.map((module, idx) => (
            <div key={idx} className="col col--4 margin-bottom--lg">
              <div className="card">
                <div className="card__header">
                  <h3>{module.title}</h3>
                </div>
                <div className="card__body">
                  <p>{module.description}</p>
                </div>
                <div className="card__footer">
                  <Link
                    className="button button--primary button--block"
                    to={module.link}>
                    Read More
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="The Hackathon Robotics Book - Your guide to AI-driven robotics.">
      <HomepageHeader />
      <main>
        <HomepageModules />
        <Chatbot />
      </main>
    </Layout>
  );
}